import re
from pylib.myParserFunctions import makeReferenceName as refName
from pylib.myParserFunctions import makeTitleCase as titleCase
#^^^do not remove pylib

def makeLink( line ):
    xml = ""
    regex_result = re.search("<link_.>(.*)</link", line)
    record_name = regex_result.group(1)                    
    record_name = record_name.replace(".webp", "")
    #external links to other mod files need "reference." at the beginning of the link
    if "@" in record_name:
        record_name, external_book = record_name.split("@")
        external_link = "reference."
        external_book = "@" + external_book
    else:
        external_link = ""; external_book = ""
    record_name = titleCase(record_name)
    record_ref_name = refName(record_name) + external_book
    xml = xml + "\t\t\t\t\t\t\t<linklist>\n"
    if line[6] == "i": #image
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"imagewindow\" recordname=\""
        xml = xml + f"{external_link}image.{record_ref_name[4:]}\">Image: {record_name[4:]}</link>\n"
    elif line[6] == "a": #ancestry
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"race\" recordname=\"{external_link}race.{record_ref_name}\""
        xml = xml + f">Ancestry: {record_name}</link>\n"
    elif line[6] == "n" and external_link == "": #npc
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"npc\" recordname=\""
        xml = xml + f"npc.{record_ref_name}\">NPC: {record_name}</link>\n"
    elif line[6] == "n" and external_link != "": #npc has an "s" when under <reference>
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"npc\" recordname=\""
        xml = xml + f"{external_link}npcs.{record_ref_name}\">NPC: {record_name}</link>\n"
    elif line[6] == "s": #spell
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"power\" recordname=\""
        xml = xml + f"{external_link}power.{record_ref_name}\">Spell: {record_name}</link>\n"
    elif line[6] == "t": #table
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"table\" recordname=\""
        xml = xml + f"{external_link}tables.{record_ref_name}\">Table: {record_name}</link>\n"
    elif line[6] == "T": #talent
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"talent\" recordname=\""
        xml = xml + f"{external_link}talent.{record_ref_name}\">Talent: {record_name}</link>\n"
    elif line[6] == "e": #encounter
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"battle\" recordname=\""
        xml = xml + f"battle.{record_ref_name}\">Encounter: {record_name}</link>\n"                    
    elif line[6] == "m": #item
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"item\" recordname=\""
        xml = xml + f"{external_link}item.{record_ref_name}\">Item: {record_name}</link>\n"
    elif line[6] == "p": #parcel
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"treasureparcel\" recordname=\""
        xml = xml + f"treasureparcels.{record_ref_name}\">Parcel: {record_name}</link>\n"
    elif line[6] == "r": #random encounter
        xml = xml + "\t\t\t\t\t\t\t\t<link class=\"battlerandom\" recordname=\""
        xml = xml + f"battlerandom.{record_ref_name}\">Encounter: {record_name}</link>\n"
    else:
        print("ERROR: Cannot proccess link", line)
        raise
    xml = xml + "\t\t\t\t\t\t\t</linklist>\n"
    return xml

if __name__ == "__main__":
    x = "<link_n>Bob</link_n>"
    print(makeLink(x))
