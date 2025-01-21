###############
#
# Copy an xml file with talents into temp_in
#
################

import os
import re

in_dir = os.getcwd() + "\\temp_in\\"
out_dir = os.getcwd() + "\\temp_out\\"

for file_name in os.listdir(in_dir):
    input_file = os.path.join(in_dir, file_name)
    with open(input_file, 'r', encoding='utf-8') as file:
        xml_contents = file.read()
    xml_contents = xml_contents.replace("\t\n", "")
    # Replace every line starting with one tab with an empty string
    pattern = r"^\t<.*\n"
    xml_contents = re.sub(pattern, "", xml_contents, flags=re.MULTILINE)
    xml_lines = xml_contents.split("\n")
    tag = ""
    for line in xml_lines:
        if line == "": continue
        #check for end tag
        if tag != "":
            regex_result = re.match(f"\t\t</{tag}>", line)
            if regex_result:
                fh_out.write(line + "\n")
                fh_out.close()
                tag = ""
                continue
        #check for start tag
        regex_result = re.match(r"\t\t<(.*)>", line)
        if regex_result: #start a new item
            tag = regex_result.group(1)
            print(tag)
            output_file = os.path.join(out_dir, tag + ".xml")
            fh_out = open(output_file, 'w', encoding='utf-8')
            fh_out.write(line + "\n")
            continue
        #continue with the currently open item
        fh_out.write(line + "\n")
