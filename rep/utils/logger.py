import logging

def configure_logging():
    logging.basicConfig(level=logging.INFO, 
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S")
    logging.info("Configured logging")
