import json
from pathlib import Path
from pylib.myParserFunctions import makeReferenceName as refName
from pylib.myParserFunctions import addSpaces as addSpace
import logger as lg
import sys
import re

class Converter:
    #an instance consists of a single conversion
    #attributes: in_file (.json), xml_data, error_report (.txt)
    #methods: convert2FG: creates the xml_data attribute from the in_file

    #intialize class data <<<< reminder: class level attributes need the class name in front, e.g. Converter.source_dic

    #The following spells are in both the wizard list and the priest list
    duplicate_spells_list = ["speak_with_dead", "protection_from_evil", "plane_shift", "light", "control_water"]
    duplicate_spells = set(duplicate_spells_list)

    full_stat_dic = {'CHA':'charisma','CON':'constitution','DEX':'dexterity','INT':'intelligence','STR':'strength','WIS':'wisdom'}

    stat_bonus_dic = {
        "1":"-4","2":"-4","3":"-4","4":"-3","5":"-3",
        "6":"-2","7":"-2","8":"-1","9":"-1","10":"0",
        "11":"0","12":"1","13":"1","14":"2","15":"2",
        "16":"3","17":"3","18":"4","19":"4","20":"4"}

    #source_dic tracks which book something came from
    source_dic = {}
    in_file = Path.cwd() / 'data' / "sources.txt"
    with open(in_file, "r") as fh_in:
        lines = fh_in.readlines()
    for line in lines:
        if line[0] == "#": continue 
        line = line.strip()
        item, source = line.split("\t")
        source_dic[item] = source

    #advanced effects dictionary
    #lists effects text associated the abilities
    #source | [effect text]
    # Elf | [ATK: 1, ranged]\n[SPELLCAST: 1]
    adveffects_dic = {}
    in_file = Path.cwd() / 'data' / "adveffects.txt"
    with open(in_file, "r") as fh_in:
        lines = fh_in.readlines()
    for line in lines:
        if line[0] == "#": continue 
        line = line.strip()
        source, effect_string = line.split("\t")
        adveffects_dic[source] = effect_string

    #rolled talents dictionary
    #JSON file differentiates between class talents and bonus talents
    #bonus talents are from patrons, black lotus, etc.
    #these are grouped together in FG
    #map the JSON rolled talents / bonus talents to the FG rolled talents
    #JSON name | FG name
    #Fighter ArmorMastery | fighter_improved_ac.xml
    talents_folder = Path.cwd() / 'data' / 'talents'
    rolled_talents_dic = {}
    in_file = Path.cwd() / 'data' / "rolled_talents.txt"
    with open(in_file, "r") as fh_in:
        lines = fh_in.readlines()
    for line in lines:
        if line[0] == "#": continue 
        line = line.strip()
        json_name, fg_name = line.split("\t")
        rolled_talents_dic[json_name] = fg_name

    #registry
    #a set containing all of the names of items and spells
    #stores the reference name version
    #list is contents of the data/items/ and data/spells/ folders
    registry = set()
    items_folder = Path.cwd() / 'data' / 'items'
    for xml_file in items_folder.iterdir():
        registry.add(xml_file.stem)
    spells_folder = Path.cwd() / 'data' / 'spells'
    for xml_file in spells_folder.iterdir():
        registry.add(xml_file.stem)

    def __init__(self, log):
        self.json_file = "" #.json file from Shadowdarklings
        self.xml_data = "" #xml for Fantasy Grounds
        self.error_report = "" #txt file of errors that occured on conversion
        log.debug("Converter class initialized.")
        log.debug(f"Current working directory: {Path.cwd()}")
        #weapons attack list
        #keep track of the items in inventory that have "equip" capability
        #add to the attacks section of the character sheet
        self.weapons_attack_list = [] #a list of xml data

    def writeStat(self, name, number, base_score):
        stat = name
        stat_score = str(number)
        stat_bonus = Converter.stat_bonus_dic[stat_score]
        stat_base = base_score
        self.xml_data = self.xml_data + f"\t\t\t<{stat}>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<bonus type=\"number\">{stat_bonus}</bonus>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<score type=\"number\">{stat_score}</score>\n"
        self.xml_data = self.xml_data + f"\t\t\t</{stat}>\n"
        self.xml_data = self.xml_data + f"\t\t\t<{stat}_base>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<score type=\"number\">{stat_base}</score>\n"
        self.xml_data = self.xml_data + f"\t\t\t</{stat}_base>\n"
        self.xml_data = self.xml_data + f"\t\t\t<{stat}_effects>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<score type=\"number\">0</score>\n"
        self.xml_data = self.xml_data + f"\t\t\t</{stat}_effects>\n"

    def convert2FG(self, log):
        with open(self.json_file, "r") as fh:
            character_data = json.load(fh)
        name = character_data['name']
        if name == "":
            log.warning("Character has no name. Name set to [no name].")
            name = "[no name]"
        #header
        self.xml_data = self.xml_data + "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
        self.xml_data = self.xml_data + "<root version=\"4.5\" dataversion=\"20230911\" release=\"1|CoreRPG:6\">\n"
        self.xml_data = self.xml_data + "\t<character>\n"
        self.xml_data = self.xml_data + "\t\t<abilities>\n"
        #stats
        stats_dic = character_data['stats']
        stats_base_dic = character_data['rolledStats']
        for stat in stats_dic.keys():
            stat_score = stats_dic[stat]
            base_score = stats_base_dic[stat]
            full_stat = Converter.full_stat_dic[stat]
            self.writeStat(full_stat, stat_score, base_score)
        self.xml_data = self.xml_data + "\t\t</abilities>\n"
        #AC
        ac = character_data['armorClass']
        self.xml_data = self.xml_data + f"\t\t<ac type=\"number\">{ac}</ac>\n"
        #advanced effects
        ancestry = character_data['ancestry']
        adveffects_string = Converter.adveffects_dic.get(ancestry, "") #return empty string if none listed in dic
        #<adveffects type="string">[ATK: 1, ranged]\n[SPELLCAST: 1]</adveffects>
        self.xml_data = self.xml_data + f"\t\t<adveffects type=\"string\">{adveffects_string}</adveffects>\n"
        #alignment
        alignment = character_data['alignment']
        self.xml_data = self.xml_data + f"\t\t<alignment type=\"string\">{alignment}</alignment>\n"
        #background
        background = character_data['background']
        background_source = Converter.source_dic.get(background, "ERROR")
        if background_source == "ERROR":
            log.error(f"Background not recognized: {background}.")
            log.debug(f"source_dic dump:\n{json.dumps(Converter.source_dic, indent=4)}")
            self.xml_data = self.xml_data + f"\t\t<background type=\"string\">{background} (ERROR: NO SOURCE)</background>\n"
        else:
            background_link = refName(background) + "@" + background_source
            self.xml_data = self.xml_data + f"\t\t<background type=\"string\">{background}</background>\n"
            self.xml_data = self.xml_data + "\t\t<backgroundlink type=\"windowreference\">\n"
            self.xml_data = self.xml_data + "\t\t\t<class>reference_background</class>\n"
            self.xml_data = self.xml_data + f"\t\t\t<recordname>reference.background.{background_link}</recordname>\n"
            self.xml_data = self.xml_data + "\t\t</backgroundlink>\n"
        #title
        title = character_data['title']
        self.xml_data = self.xml_data + f"\t\t<char_title type=\"string\">{title}</char_title>\n"
        #class and ancestry; if not registered in source_dic then change to "ERROR"
        pc_class = character_data['class']
        pc_class_source = Converter.source_dic.get(pc_class, "ERROR")
        if pc_class_source == "ERROR":
            log.error("Class not recognized: {pc_class}.")
            log.debug(f"source_dic dump:\n{json.dumps(Converter.source_dic, indent=4)}")
            pc_class = "ERROR"
        pc_class_reference_name = refName(pc_class)
        ancestry = character_data['ancestry']
        ancestry_source = Converter.source_dic.get(ancestry, "ERROR")
        if ancestry_source == "ERROR":
            log.error(f"Ancestry not recognized: {ancestry}.")
            log.debug(f"source_dic dump:\n{json.dumps(Converter.source_dic, indent=4)}")
            ancestry = "ERROR"
        ancestry_reference_name = refName(ancestry)
        self.xml_data = self.xml_data + f"\t\t<class type=\"string\">{pc_class}</class>\n"
        in_file = Path.cwd() / 'data' / 'abilities' / f"class_abilities_{pc_class_reference_name}.xml"
        with open(in_file, "r") as fh_in:
            class_abilities_xml = fh_in.read()
        in_file = Path.cwd() / 'data' / 'abilities' / f"ancestry_abilities_{ancestry_reference_name}.xml"
        with open(in_file, "r") as fh_in:
            ancestry_abilities_xml = fh_in.read()
        self.xml_data = self.xml_data + "\t\t<classabilitylist>\n"
        self.xml_data = self.xml_data + class_abilities_xml
        self.xml_data = self.xml_data + ancestry_abilities_xml
        self.xml_data = self.xml_data + "\t\t</classabilitylist>\n"
        self.xml_data = self.xml_data + "\t\t<classlink type=\"windowreference\">\n"
        self.xml_data = self.xml_data + "\t\t\t<class>reference_class</class>\n"
        self.xml_data = self.xml_data + f"\t\t\t<recordname>reference.class.{pc_class_reference_name}@{pc_class_source}</recordname>\n"
        self.xml_data = self.xml_data + "\t\t</classlink>\n"
        #coins
        gold = character_data['gold']
        silver = character_data['silver']
        copper = character_data['copper']
        self.xml_data = self.xml_data + "\t\t<coins>\n"
        self.xml_data = self.xml_data + "\t\t\t<id-00001>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<amount type=\"number\">{gold}</amount>\n"
        self.xml_data = self.xml_data + "\t\t\t\t<name type=\"string\">GP</name>\n"
        self.xml_data = self.xml_data + "\t\t\t</id-00001>\n"
        self.xml_data = self.xml_data + "\t\t\t<id-00002>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<amount type=\"number\">{silver}</amount>\n"
        self.xml_data = self.xml_data + "\t\t\t\t<name type=\"string\">SP</name>\n"
        self.xml_data = self.xml_data + "\t\t\t</id-00002>\n"
        self.xml_data = self.xml_data + "\t\t\t<id-00003>\n"
        self.xml_data = self.xml_data + f"\t\t\t\t<amount type=\"number\">{copper}</amount>\n"
        self.xml_data = self.xml_data + "\t\t\t\t<name type=\"string\">CP</name>\n"
        self.xml_data = self.xml_data + "\t\t\t</id-00003>\n"
        self.xml_data = self.xml_data + "\t\t</coins>\n"
        #encumbrance
        gear_load = character_data['gearSlotsUsed']
        gear_load_max = character_data['gearSlotsTotal']
        self.xml_data = self.xml_data + "\t\t<encumbrance>\n"
        self.xml_data = self.xml_data + f"\t\t\t<load type=\"number\">{gear_load}</load>\n"
        self.xml_data = self.xml_data + "\t\t</encumbrance>\n"
        self.xml_data = self.xml_data + f"\t\t<encumbranceallowed type=\"number\">{gear_load_max}</encumbranceallowed>\n"
        #experience
        pc_level = character_data['level']
        current_xp = character_data['XP']
        self.xml_data = self.xml_data + f"\t\t<exp type=\"number\">{current_xp}</exp>\n"
        self.xml_data = self.xml_data + f"\t\t<expneeded type=\"number\">{pc_level}0</expneeded>\n"
        #hit points
        hit_points_total = character_data['maxHitPoints']
        self.xml_data = self.xml_data + "\t\t<hp>\n"
        self.xml_data = self.xml_data + "\t\t\t<temporary type=\"number\">0</temporary>\n"
        self.xml_data = self.xml_data + f"\t\t\t<total type=\"number\">{hit_points_total}</total>\n"
        self.xml_data = self.xml_data + f"\t\t\t<wounds type=\"number\">0</wounds>\n"
        self.xml_data = self.xml_data + "\t\t</hp>\n"
        #inventory
        item_list = character_data['gear']
        self.xml_data = self.xml_data + "\t\t<inventorylist>\n"
        for item in item_list:
            item_name = item['name']
            item_count = item['quantity']
            item_ref_name  = refName(item_name)
            #read in the xml version of the item, if it exists
            if item_ref_name in Converter.registry:
                with open(Converter.items_folder / f"{item_ref_name}.xml", "r", encoding = "utf-8") as fh_in:
                    item_xml = fh_in.read()
            else:
                log.error(f"Item not recognized: {item_name}.")
                log.debug(f"xml data exists for the following Items and Spells:")
                log.debug(f"registry dump:\n{json.dumps(list(Converter.registry), indent=4)}")
                with open(Converter.items_folder / "error.xml", "r", encoding = "utf-8") as fh_in:
                    item_xml = fh_in.read()
                #add the item name to the xml
                item_xml = item_xml.replace("QQQ", item_name)
                item_xml = item_xml.replace("qqq", item_ref_name)
            #add the carried status before item cost
            #if it is a an item with an "attacktype" then it should be equipped and added to the attacks section on the main tab
            if "attacktype" in item_xml:
                item_carried_xml = f"\t\t\t\t<carried type=\"number\">2</carried>\n\t\t\t\t<cost "
            else:
                item_carried_xml = f"\t\t\t\t<carried type=\"number\">1</carried>\n\t\t\t\t<cost "
            item_xml = item_xml.replace("\t\t\t\t<cost ", item_carried_xml)
            #add the count after item cost
            item_count_xml = f"</cost>\n\t\t\t\t<count type=\"number\">{item_count}</count>\n"
            item_xml = item_xml.replace("</cost>\n", item_count_xml)
            #if the item has attack capability, then create the attack xml and store in attacks list
            attack_xml = self.convertItem2Attack(item_xml) #returns False if no attack capability
            if attack_xml: self.weapons_attack_list.append(attack_xml)
            self.xml_data = self.xml_data + item_xml
        #end for
        #end for item
        self.xml_data = self.xml_data + "\t\t</inventorylist>\n"
        #languages
        languages = character_data['languages']
        languages_list = languages.split(", ")
        self.xml_data = self.xml_data + "\t\t<languagelist>\n"
        for i, language in enumerate(languages_list, start=1):
            self.xml_data = self.xml_data + f"\t\t\t<id-0000{i}>\n"
            self.xml_data = self.xml_data + f"\t\t\t\t<name type=\"string\">{language}</name>\n"
            self.xml_data = self.xml_data + f"\t\t\t</id-0000{i}>\n"
        self.xml_data = self.xml_data + "\t\t</languagelist>\n"
        #level
        level = character_data['level']
        self.xml_data = self.xml_data + f"\t\t<level type=\"number\">{level}</level>\n"
        #luck
        self.xml_data = self.xml_data + f"\t\t<luck type=\"number\">0</luck>\n"
        #name
        name = character_data['name']
        self.xml_data = self.xml_data + f"\t\t<name type=\"string\">{name}</name>\n"
        #notes
        notes = ""
        deity = character_data['deity']
        notes = notes + f"Deity: {deity}\\n"
        #add the bonuses stored in character_data['bonuses'] to Notes
        bonuses_list = character_data['bonuses']
        for bonus in bonuses_list:
            b_name = bonus['name']
            b_bonus_name = bonus['bonusName']
            b_bonus_to = bonus['bonusTo']
            if b_bonus_name != "" and (b_name != b_bonus_name or b_bonus_to != ""):
                #looks like extra information; add to the dictionary
                bonus_text = addSpace(b_bonus_name)
                if b_bonus_to != "":
                    bonus_text = bonus_text + ": " + b_bonus_to
                    notes = notes + f"{bonus_text}\\n"
        #end for
        self.xml_data = self.xml_data + f"\t\t<notes type=\"string\">{notes}</notes>\n"
        #portrait
        self.xml_data = self.xml_data + f"\t\t<portrait type=\"token\"></portrait>\n"
        #ancestry
        self.xml_data = self.xml_data + f"\t\t<race type=\"string\">{ancestry}</race>\n"
        ancestry_reference = refName(ancestry)
        ancestry_source = Converter.source_dic.get(ancestry, "ERROR")
        #ancestry error already logged
        if ancestry_source != "ERROR":
            self.xml_data = self.xml_data + "\t\t<racelink type=\"windowreference\">\n"
            self.xml_data = self.xml_data + "\t\t\t<class>reference_race</class>\n"
            self.xml_data = self.xml_data + f"\t\t\t<recordname>reference.race.{ancestry_reference}@{ancestry_source}</recordname>\n"
            self.xml_data = self.xml_data + "\t\t</racelink>\n"
        #spells
        spells = character_data['spellsKnown']
        if spells != "None":   
            spells_list = spells.split(", ")
            self.xml_data = self.xml_data + "\t\t<spelllist>\n"
            for spell_name in spells_list:
                spell_ref_name  = refName(spell_name)
                if spell_ref_name in Converter.duplicate_spells: #light -> light_wizard
                    spell_ref_name = spell_ref_name + "_" + pc_class_reference_name
                #read in the xml version of the spell, if it exists
                if spell_ref_name in Converter.registry:
                    with open(Converter.spells_folder / f"{spell_ref_name}.xml", "r", encoding = "utf-8") as fh_in:
                        spell_xml = fh_in.read()
                else:
                    log.error(f"Spell not recognized: {spell_name}; reference_name: {spell_ref_name}.")
                    log.debug(f"xml data exists for the following Items and Spells:")
                    log.debug(f"registry dump:\n{json.dumps(list(Converter.registry), indent=4)}")
                    with open(Converter.spells_folder / "error.xml", "r", encoding = "utf-8") as fh_in:
                        spell_xml = fh_in.read()
                    #add the spell name to the xml
                    spell_xml = spell_xml.replace("QQQ", spell_name)
                    spell_xml = spell_xml.replace("qqq", spell_ref_name)
                self.xml_data = self.xml_data + spell_xml
            self.xml_data = self.xml_data + "\t\t</spelllist>\n"
        #end if
        #level up talents
        #there are duplicates in the JSON file
        #to avoid adding duplicates, track already added talents in a set
        already_added_talent_set = set()
        self.xml_data = self.xml_data + "\t\t<talentlist>\n"
        #talents have two scorces: ['levels'] and ['bonuses']
        level_talents_list = character_data['levels']
        for talent in level_talents_list:
            #check for the special case of rolled a 12 on a ptron boon table
            #since such a result si recorded seperately
            rolled12 = talent['Rolled12TalentOrTwoStatPoints']
            if rolled12 != "":
                talent_name = "TalentChoiceOrTwoStatPoints"
            else:
                talent_name = talent['talentRolledName']
            if talent_name != "":
                talent_full_name = f"{pc_class} {talent_name}"
                if talent_full_name not in already_added_talent_set:
                    already_added_talent_set.add(talent_full_name)
                    fg_talent_name = Converter.rolled_talents_dic.get(talent_full_name, "ERROR")
                    if fg_talent_name == "ERROR":
                        log.error(f"Standard Talent not recognized: {talent_full_name}.")
                        log.debug(f"rolled_talents_dic dump:\n{json.dumps(Converter.rolled_talents_dic, indent=4)}")
                        with open(Converter.talents_folder / "error.xml", "r", encoding = "utf-8") as fh_in:
                            talent_xml = fh_in.read()
                        #add the item name to the xml
                        talent_ref_name = refName(talent_name)
                        talent_xml = talent_xml.replace("QQQ", talent_full_name)
                        talent_xml = talent_xml.replace("qqq", talent_ref_name)
                    else:
                        with open(Converter.talents_folder / f"{fg_talent_name}.xml", "r", encoding = "utf-8") as fh_in:
                            talent_xml = fh_in.read()
                    self.xml_data = self.xml_data + talent_xml
        #end for
        bonus_talents_list = character_data['bonuses']
        for talent in bonus_talents_list:
            #check for the special case of rolled a 12 on a ptron boon table
            #since such a result is recorded seperately
            talent_name = talent['name']
            patron = talent.get('boonPatron', "")
            if talent_name != "" and patron != "":
                talent_full_name = f"{patron} {talent_name}"
                if talent_full_name not in already_added_talent_set:
                    already_added_talent_set.add(talent_full_name)
                    fg_talent_name = Converter.rolled_talents_dic.get(talent_full_name, "ERROR")
                    if fg_talent_name == "ERROR":
                        log.error(f"Bonus Talent not recognized: {talent_full_name}.")
                        log.debug(f"rolled_talents_dic dump:\n{json.dumps(Converter.rolled_talents_dic, indent=4)}")
                        with open(Converter.talents_folder / "error.xml", "r", encoding = "utf-8") as fh_in:
                            talent_xml = fh_in.read()
                        #add the item name to the xml
                        talent_ref_name = refName(talent_name)
                        talent_xml = talent_xml.replace("QQQ", talent_full_name)
                        talent_xml = talent_xml.replace("qqq", talent_ref_name)
                    else:
                        with open(Converter.talents_folder / f"{fg_talent_name}.xml", "r", encoding = "utf-8") as fh_in:
                            talent_xml = fh_in.read()
                    self.xml_data = self.xml_data + talent_xml
        self.xml_data = self.xml_data + "\t\t</talentlist>\n"
        #weapons list
        if len(self.weapons_attack_list) == 0:
            self.xml_data = self.xml_data + "\t\t<weaponlist />\n"
        else:
            self.xml_data = self.xml_data + "\t\t<weaponlist>\n"
            for w in self.weapons_attack_list:
                self.xml_data = self.xml_data + w
        self.xml_data = self.xml_data + "\t\t</weaponlist>\n"
        self.xml_data = self.xml_data + "\t</character>\n"
        self.xml_data = self.xml_data + "</root>\n"
    #endfor

    def convertItem2Attack(self, item_xml):
        unneeded_attribute_list = [
            "attacktype", "cost", "description", "p", "/description",
            "loading", "range", "weight", "picture", "nonid_name",
            "nonidentified", "weight"
            ]
        if "attacktype" not in item_xml: return False
        attack_xml = item_xml
        #remove the unneeded lines
        for a in unneeded_attribute_list:
            target_string = rf"\t+<{a}.*\n"
            attack_xml = re.sub(target_string, "", attack_xml)
        #add the needed lines
        #add <hands> = 0 after <finesse>; single handed attack
        new_xml = "</finesse>\n\t\t\t\t<hands type=\"number\">0</hands>\n"
        attack_xml = attack_xml.replace("</finesse>\n", new_xml)
        #add <maxammo> = 0 after <item_attack_bonus>
        new_xml = "</item_attack_bonus>\n\t\t\t\t<maxammo type=\"number\">0</maxammo>\n"
        attack_xml = attack_xml.replace("</item_attack_bonus>\n", new_xml)
        #add <meleerange> before <name>; 0 = melee; 1 = ranged
        if "Ranged" in item_xml:
            melee_or_ranged = 1
        elif "Melee" in item_xml:
            melee_or_ranged = 0
        else:
            #unable to determine if the weapon is ranged or melee
            #report error and default to melee
            regex_result = re.search(r">(.*?)</name>", item_xml)
            if regex_result:
                item_name = regex_result.group(1)
            else:
                item_name = "MISSING NAME"
            log.error(f"Unable to determine attack type for {item_name}; set to melee.")
            melee_or_ranged = 0
        new_xml = f"\t\t\t\t<meleerange type=\"number\">{melee_or_ranged}</meleerange>\n\t\t\t\t<name "
        attack_xml = attack_xml.replace("\t\t\t\t<name ", new_xml)
        #add <shortcut> after <name>
        regex_result = re.match(r"\t\t\t<(.*)>", item_xml)
        item_reference_name = regex_result.group(1)
        new_xml = "</name>\n\t\t\t\t<shortcut type=\"windowreference\">\n"
        new_xml = new_xml + "\t\t\t\t\t<class>item</class>\n"
        new_xml = new_xml + f"\t\t\t\t\t<recordname>....inventorylist.{item_reference_name}</recordname>\n"
        new_xml = new_xml + f"\t\t\t\t</shortcut>\n"
        attack_xml = attack_xml.replace("</name>\n", new_xml)
        return attack_xml

####################################

if __name__ == "__main__":
    #look for JSON files in the in-folder, and convert one at a time
    in_folder = Path.cwd() / 'in'
    out_folder = Path.cwd() / 'out'
    files = [f for f in in_folder.iterdir() if f.is_file() and f.suffix == ".json"]
    if len(files) == 0:
        print("No files to convert.")
        sys.exit()
    for file in files:
        #these are file names only
        character_name = file.stem
        log = lg.createLogger(character_name, "development")
        log.debug(f"Converting {character_name}.")
        c = Converter( log )
        c.json_file = file
        c.convert2FG( log )
        with open(out_folder / f"{character_name}.xml", "w", encoding = "utf-8") as fh_out:
            fh_out.write(c.xml_data)
        #sys.exit() #exit after converting only one file
