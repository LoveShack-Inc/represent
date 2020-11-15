import argparse
import logging
import time
import sys

from rep.dao.VoteObjectDao import VoteObjectDao
from rep.crawlers import get_crawlers
from rep.processors import get_processor_map
from rep.processors.Exceptions import PdfProcessorException

SLEEP_MINUTES = 60
SLEEP_TIME = 60 * SLEEP_MINUTES
PARSERS = get_processor_map()

voteObjectsDao = VoteObjectDao()

def main():
    logging.info("Parsing args")
    args = _parse_args()
    if args.forever:
        while True:
            logging.info("Running on loop")
            _choose_run_strategy(args)
            logging.info(f"Sleeping for {SLEEP_MINUTES} minutes")
            time.sleep(SLEEP_TIME)
    else:
        logging.info("Running once")
        _choose_run_strategy(args)
        logging.info("Exiting")


def _parse_args():
    parser = argparse.ArgumentParser(description='Crawl for represenation data.')

    parser.add_argument('--forever', default=False, action='store_true', 
        help='Run the indefinitely. Default behavior is to run just once')

    parser.add_argument('--crawl', default=False, action='store_true', 
        help='Option to crawl')

    parser.add_argument('--process', default=False, action='store_true', 
        help='Option to parse crawled vote object blobs')

    return parser.parse_args()



def _choose_run_strategy(args):
    if args.crawl and args.process:
        logging.error("Choose --crawl or --process, not both")
    elif args.crawl:
        _run_crawlers()
    elif args.process:
        _run_processors()
    else:
        logging.error("Supply --crawl or --process")
        sys.exit(0)


def _run_crawlers():
    for i in get_crawlers():
        try:
            i.crawl()
        except Exception as e:
            logging.exception("An exception occurred during crawler execution")

def _run_processors():
    unprocessed_objects = voteObjectsDao.getUnprocessed()
    for i in unprocessed_objects:
        try:
            parser = PARSERS[f"{i.sourceFormat}&&{i.sourceType}"]
            parser.process_blob(i.blob)
        except AttributeError as e:
            logging.exception(
                f"Skipping record. No processor exists for [format={i.sourceFormat}, type={i.sourceType}, url={i.sourceUrl}]"
            )
        except PdfProcessorException as e:
            logging.exception(
                f"Skipping record. We failed to process the PDF [format={i.sourceFormat}, type={i.sourceType}, url={i.sourceUrl}]"
            )
