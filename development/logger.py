import logging

def createLogger(character_name, logging_level):
    # Create a logger object with name = character_name
    logger = logging.getLogger(character_name)
    if logging_level == "development":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    # Create handlers
    console_handler = logging.StreamHandler()  # Logs to console
    file_handler = logging.FileHandler('log.txt')  # Logs to file
    # Set logging levels for handlers
    console_handler = logging.StreamHandler() #without this errors by default go to sys.stderr
    console_handler.setLevel(logging.CRITICAL + 1)  # Set level higher than CRITICAL to suppress all messages
    file_handler.setLevel(logging.DEBUG)
    # Create the formatter
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

def get_log_file_path(logger):
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename  # This contains the file path
    return None

if __name__ == "__main__":
    # Test the logger code
    #CRITICAL > ERROR > WARNING > INFO > DEBUG
    log = createLogger("Bobby", "development")
    log.debug("This is a debug message.")
    log.info("This is an info message..")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
    print(get_log_file_path(log))
    
