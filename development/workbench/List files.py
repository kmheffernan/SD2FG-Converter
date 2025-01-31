import os
import re

##folder = os.getcwd() + "//temp_in//"
##for file in os.listdir(folder):
##    print(f"\"{file}\"")
    
in_dir = os.getcwd() + "\\temp_in\\"
out_dir = os.getcwd() + "\\temp_out\\"

for file_name in os.listdir(in_dir):
    regex_result =  re.match(r"ancestry_abilities_(.*)\.xml", file_name)
    ancestry = regex_result.group(1)
    input_file = os.path.join(in_dir, file_name)
    with open(input_file, 'r', encoding='utf-8') as file:
        xml_contents = file.read()
    regex_result = re.match(r"\t\t\t<(.*)>", xml_contents)
    talent = regex_result.group(1)
    print(f"{ancestry}_{talent}")
    
    
