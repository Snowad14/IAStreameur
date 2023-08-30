import logging

def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f'\033[92m%(asctime)s\033[0m - \033[94m%(name)s - %(levelname)s\033[0m - %(message)s') 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(lambda record: record.name == 'AIStreamer')
    logger.addHandler(console_handler)
    badLoggers = ["faiss.loader", "fairseq.tasks.hubert_pretraining", __name__, "twitchio.websocket"]
    for logName in badLoggers:
        logging.getLogger(logName).setLevel(logging.CRITICAL)
    return logger