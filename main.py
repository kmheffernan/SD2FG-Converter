from pathlib import Path
import logger as lg
import converter as cv
import interface as it
import sys

############################
# This project is licensed under the Creative Commons Attribution-NonCommercial 4.0\nInternational License.
# See the License file for details.
############################

def skipGUI(log_level):
    in_folder = Path.cwd() / 'in'
    out_folder = Path.cwd() / 'out'
    json_files = [file for file in in_folder.iterdir() if file.is_file() and file.suffix == '.json']
    if len(json_files) == 0:
        with open(Path.cwd() / "log.txt", "w", encoding = "utf-8") as fh_out:
            fh_out.write("No files with .json extension found in in folder. Program terminated.")
            sys.exit()
    for json_file in json_files:
        character_name = json_file.stem
        log = lg.createLogger(character_name, log_level)
        log.debug(f"Converting {character_name}.")
        log.debug("Setting \'use_gui\' = \'no\' detected. GUI not used.")
        c = cv.Converter(log)
        c.json_file = json_file
        c.convert2FG( log )
        if Path(out_folder).exists():
            with open(out_folder / f"{character_name}.xml", "w", encoding = "utf-8") as fh_out:
                fh_out.write(c.xml_data)
        else:
            log.error(f"Folder {out_folder} does not exist.")

#Handle the settings
settings_dic = {'keep_log':'no', 'report_level':'production', 'use_gui':'yes', 'save_path':''}
user_settings_file = 'settings.txt'
if Path(user_settings_file).exists():
    with open(user_settings_file, 'r') as fh_in:
        lines = fh_in.readlines()
    for line in lines:
        if line[0] == "#": continue
        line = line.strip()
        setting, paramater = line.split("=")
        settings_dic[setting] = paramater

#Delete the old log file
log_file = Path.cwd() / "log.txt"
if settings_dic['keep_log'] == 'no':
    if Path(log_file).exists():
        log_file.unlink()

#Initialize logger
if settings_dic['report_level'] == 'development':
    log_level = "development"
else:
    log_level = "production"

#Initialize interface for user to select input file
if settings_dic['use_gui'] == 'no':
    skipGUI(log_level)
else:
    json_file = it.get_json_file_window() #returns a path object
    if not json_file:
        sys.exit()
    #get_file_window returns a path object
    #Use the file name stem as the name for the logger
    character_name = json_file.stem
    log = lg.createLogger(character_name, log_level)
    log.debug(f"Converting {character_name}.")
    log.debug("Setting \'use_gui\' = \'yes\' detected. GUI used.")
    if not json_file.suffix or json_file.suffix.lower() != ".json":
        log.error("File extension not \".json\".")
        sys.exit()
    c = cv.Converter( log )
    c.json_file = json_file
    log.debug(f"Target .json file: {c.json_file}.")
    #Convert file
    c.convert2FG( log )
    #Generate the log text for the GUI window
    log_file_path = lg.get_log_file_path(log)
    with open(log_file_path, "r", encoding = "utf-8") as fh_in:
        log_text_lines = fh_in.readlines()
    #keep  the warnings and errors
    log_text = ""
    for line in log_text_lines:
        if "WARNING" in line or "ERROR" in line:
            character_name, message = line.split(" - ", 1)
            message = message.replace(" - ", ": ")
            log_text = log_text + message
    if log_text == "":
        log_text = "No warnings / errors."
    log.debug(f"Log text passed to confirm_save_window: {log_text}.")
    #Initialize interface for user to select save path
    if settings_dic['save_path'] == '':
        log.debug("Setting \'save_path\' not detected. Use GUI to confirm save path.")
        #get save path from user
        log.debug(f"Initial save path set to \'{c.json_file}\'")
        save_location = it.confirm_save_window( str(c.json_file.parent), log_text )
        if not save_location:
            sys.exit()
    else:
        #use save path from settings file
        save_location = settings_dic['save_path']
        if not Path(save_location).exists():
            log.error(f"Path not found: {save_location}")
            sys.exit()
    #convert strings to paths
    save_file = f'{character_name}.xml'
    save_path = Path(save_location)
    with open(save_path / save_file, "w", encoding = "utf-8") as fh_out:
        fh_out.write(c.xml_data)
