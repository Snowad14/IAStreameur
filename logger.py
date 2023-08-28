import logging

def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f'\033[92m%(asctime)s\033[0m - \033[94m%(name)s - %(levelname)s\033[0m - %(message)s') 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger