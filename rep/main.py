import argparse
import logging
from rep.dataclasses.RepresentativeInfo import RepresentativeInfo
import time
import sys
import os

from rep.dao.PagedQueryHelper import iterate_through_paged_query
from rep.dao.VoteObjectDao import VoteObjectDao
from rep.crawlers import get_crawlers
from rep.processors import get_processor_map
from rep.processors.Exceptions import PdfProcessorException
from rep.dao.ProcessedVoteResultDao import ProcessedVoteResultDao
from rep.dao.RepresentativeInfoDao import RepresentativeInfoDao

SLEEP_MINUTES = 60
SLEEP_TIME = 60 * SLEEP_MINUTES
PARSERS = get_processor_map()

voteObjectsDao = VoteObjectDao()
processedVoteResultDao = ProcessedVoteResultDao()
representativeInfoDao = RepresentativeInfoDao()

if os.getenv("ENV", "prod") == "local":
    time.sleep(10)


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
    # #########
    # Dalton's workspace, should not be committed
    representativeInfoDao._get_id_from_name('hi')


    # #########
    for i in iterate_through_paged_query(voteObjectsDao.getUnprocessed, 1):
        try:
            parser = PARSERS[f"{i.sourceFormat}&&{i.sourceType}"]
            parsed_vote = parser.process_blob(i)
            if parsed_vote is not None:
                processedVoteResultDao.write(parsed_vote)
                voteObjectsDao.markProcessedBySourceUrl(i.sourceUrl)
                logging.info('Successfully processed the following file: ' + i.sourceUrl)
            else:
                voteObjectsDao.markProcessedBySourceUrl(i.sourceUrl)
        except AttributeError as e:
            logging.exception(
                f"Skipping record. No processor exists for [format={i.sourceFormat}, type={i.sourceType}, url={i.sourceUrl}]"
            )
        except PdfProcessorException as e:
            logging.exception(
                f"Skipping record. We failed to process the PDF [format={i.sourceFormat}, type={i.sourceType}, url={i.sourceUrl}]"
            )

# I'm not sure how else to get the debugger to work
if __name__ == "__main__":
    main()
