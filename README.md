Shadowdarklings Fantasy Grounds Converter
by Kevin Heffernan

VERSION:
1.0

LICENSE:
This software is an independent product published under the Shadowdark RPG Third-Party License and is not affiliated with
The Arcane Library, LLC. Shadowdark RPG (c) 2023 The Arcane Library, LLC.
This work is freeware, and it is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/.

DISCLAIMER OF LIABILITY:
This software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

DESCRIPTION:
The purpose of this software (hereafter, the converter) is to convert the output of the website Shadowdarklings (.json file extension) to input usable by the Fantasy Grounds application (.xml file extension). This version of the converter will process data from the following sources:
Shadowdark RPG core rulebook
Cursed Scroll 1 - Diablerie
Cursed Scroll 2 - Red Sands
Cursed Scroll 3 - Midnight Sun
Unnatural Selection

The converter generates links to the Fantasy Grounds module data. The user must own the corresponding module in Fantasy Grounds in order for a link to open the linked data record.
The following data types are converted:
classes
ancestries
backgrounds
talents
spells
items, including magic items

Material outside the scope of coverage should be added to the character sheet by hand after loading into Fantasy Grounds. If such material is included in the character sheet at the time of conversion, the converter will generate warnings, and the write "ERROR" to the character sheet in place of the unrecognized data.

HOW TO USE:
1. Create a character on the Shadowdarklings website.
2. Save as a .json file to your computer.
3. Run the converter, select the .json file, and convert.
4. Choose the save destination for the .xml file.
5. Run Fantasy Grounds.
6. From the Character Selection window, choose the Import option.
7. Select and load the .xml file.

LOG:
A record of warnings and errors is kept in log.txt. The default behavior of the converter is delete this file on start up.

SETTINGS:
The file settings.txt can be edited to change the default behavior of the converter. Use hash mark (#) to comment out a setting. Remove the hash mark to apply the setting. The following settings have the describe effect:
#keep_log - do not delete log.txt on start up
#delete_log  - delete log.txt on start up
#development - report detailed debugging information to the log file
#production - report warnings and errors only to the log file
#skip_gui - do not use the graphics user interface (see below)
#use_gui - use the graphics user interface
#save_path= - set the default save folder

BATCH PROCESSING:
The default behavior of the converter is to use a graphics user interface to select and convert a single file. Turning off this interface in the settings causes the converter to convert all .json files in the in folder and write the converted .xml files to the out folder.

BUGS:
Please bugs and issues in one of the following places:

Fantasy Ground Official Shadowdark System and content thread of the sd-creators-forum within the Discord server for The Arcane Library
https://discord.com/channels/558029475837902851/1240298222321274900

The shadowdark forum of the Discord server for Fantasy Grounds
https://discord.com/channels/274582899045695488/1087432684957073418
