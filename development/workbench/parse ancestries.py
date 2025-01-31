###############
#
# Copy an xml file with ancestries into temp_in
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
    ancestry = ""
    write_out_flag = False
    talent_name_flag = False
    talent_name = ""
    for line in xml_lines:
        if line == "": continue
        #check for start of an ancestry
        regex_result = re.match(r"\t\t<([^/].*)>", line)
        if regex_result: #start a new ancestry
            tag = regex_result.group(1)
            print(tag)
            output_file = os.path.join(out_dir, f"ancestry_abilities_{tag}.xml")
            fh_out = open(output_file, 'w', encoding='utf-8')
            continue
        #check for start tag
        if line == "\t\t\t<traits>":
            write_out_flag = True
            talent_name_flag = True
        #check for end tag
        elif line == "\t\t\t</traits>":
            fh_out.close()
            write_out_flag = False
        elif write_out_flag:
            if talent_name_flag:
                regex_result = re.match(r"\t\t\t\t<([^/].*)>", line)
                talent_name = tag = regex_result.group(1)
                fh_out.write(f"\t\t\t<{talent_name}>\n")
                fh_out.write(f"\t\t\t\t<counter type=\"number\">0</counter>\n")
                fh_out.write(f"\t\t\t\t<countercheck type=\"number\">0</countercheck>\n")
                talent_name_flag = False
            elif talent_name in line:
                #we are at the end tag
                fh_out.write(f"\t\t\t</{talent_name}>\n")
            else:
                fh_out.write(line + "\n")
                
            
