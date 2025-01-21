import re

def makeReferenceName(s):
    #convert uppercase to lowercase, replace spaces with underscores, and remove apostrophes & brackets
    s = s.lower()
    s = s.replace(" ", "_")
    s = s.replace("?", "")
    s = s.replace("!", "")
    s = s.replace("\"", "")
    s = s.replace("\'", "")
    s = s.replace("/", "_")
    s = s.replace(":", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("’", "")
    s = s.replace("“", "")
    s = s.replace("”", "")
    s = s.replace(",", "")
    s = s.replace(".", "")
    s = s.replace("-", "_")
    s = s.replace("–", "_")
    s = s.replace("+", "_")
    s = s.replace("*", "")
    s = s.replace("′", "\'")
    return s

def cleanText(s):
    #replaces the slanted quotes and other special characters
    s = s.replace("’", "\"")
    s = s.replace("“", "\"")
    s = s.replace("”", "\'")
    s = s.replace("…", "...")
    return s

def containsDigit(s):
    regex_result = re.search("(\d)", s)
    if regex_result:
        return regex_result.groups()[0]
    else:
        return False

def makeTitleCase(t):
    t = t.replace("′", "\'")
    function_words = ["a", "an", "as", "at", "and", "but", "by", "for", "in", "it", "of", "or", "so", "the", "to", "with", "from", "without", "into", "yet"]
    capital_words = ["AC", "DC", "STR", "INT", "WIS", "CON", "DEX", "CHA" , "XP", "NPC", "PC", "HP", "RPG", "BW"]
    #If there is a number at the beginning of the string, remove it before processing the letters, and then add then back on at the end
    regex_result = re.search(r"(^[0-9]+[A-Z]?\. )(.*)", t) #number optionally repeated | one optional captial letter | period | space || the room title
    if regex_result:
        number = regex_result.group(1)
        t = regex_result.group(2)
    else:
        number = ""
    if t == "":
        return ""
    words = t.split(" ")
    title_case = ""
    for word in words:
        if word.lower() in function_words:
             word = word.lower()
        elif word.upper() == "NPCS":
            word = "NPCs"
        elif word.upper() in capital_words:
            word = word.upper()
        elif len(word) == 1:
            word = word.upper()
        elif word[0] == "(":
            word = "(" + word[1].upper() + word[2:].lower()
        else:
            word = word[0].upper() + word[1:].lower()
        #deal with the cases of a - and / in the word
        if "-" in word:
            a, b = word.split("-")
            word = a + "-" + b[0].upper() + b[1:].lower()
        if "/" in word:
            a, b = word.split("/")
            word = a + "/" + b[0].upper() + b[1:].lower()
        title_case = title_case + word + " "
    #the first letter must always be a capital letter
    title_case = title_case[0].upper() + title_case[1:]
    #add the number back on and return
    return number + title_case.strip()

def addSpaces(t):
    t = re.sub(r"([a-z0-9])([A-Z0-9])", r"\1 \2", t)
    #misses the second space in Word2Word; apply again
    t = re.sub(r"([a-z0-9])([A-Z0-9])", r"\1 \2", t)
    return t

if __name__ == "__main__":
##    s = "Qwert-\'Y (1)"
##    t = "THIS IS A BOOK CALLED B"
##    u = "test (qw/qw)"
##    x = "01A. THE TEN-EYED′ ORACLE"
##    z = "HP"
##    print(makeTitleCase(z)) 
##    print(makeTitleCase(x))
##    assert makeReferenceName(s) == "qwert_y_1", "Should be qwert_y_1"
##    assert containsDigit(s) == "1", "Should be 1"
##    assert makeTitleCase(t) == "This Is a Book Called B", "Should be This Is a Book Called B"
##    assert makeTitleCase(u) == "Test (Qw/Qw)"
##    assert makeTitleCase(z) == "Increased HP"
##    print("Tests passed.")
    t = "Qwerty2QwertyQwerty"
    print(addSpaces(t))
