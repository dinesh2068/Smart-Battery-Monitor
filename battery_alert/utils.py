import logging

def setup_logger():
    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

def log(message):
    logging.info(message)