import io
import PyPDF2
import re
import sys
import logging
import datetime
import time

from .Exceptions import PdfProcessorException
from .BaseProcessor import BaseProcessor


class CtGovPdfProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()

        self.YAY_OR_NAY_PATTERN = re.compile(r"(Y|N|A)\W+\d+\W+(\w+)\W+((\w)\.)?\W?(\w+)")
        self.DATE_PATTERN = r"(Taken on )(.*?)( )"
        self.VOTE_FOR_PATTERN = r"(Vote for )(.*?)( Seq)"

    def process_blob(self, blob, source_url):
        try: 
            return self._process_blob_wrapper(blob, source_url)
        except Exception as e:
            raise PdfProcessorException("An exception occurred while processing a  file")
    
    def _process_blob_wrapper(self, blob, source_url):
        page_content = self._get_page_from_blob(blob)

        votes = re.findall(self.YAY_OR_NAY_PATTERN, page_content)
        date_list = re.findall(self.DATE_PATTERN, page_content)
        num_list = re.findall(self.VOTE_FOR_PATTERN, page_content)
        year = source_url.split('/')[3]

        # Length of the vote list and/or num_list will be 0 (or 1) if the PDF isn't a vote file that we know
        # how to read
        if len(votes) <= 1 or len(num_list) <= 0:
            logging.error('PDF file is not one of the understood formats')
            return None

        vote_list = []
        for i in range(len(votes)):
            rep_vote = votes[i][0]
            rep_name = ' '.join([i for i in [votes[i][1], votes[i][3], votes[i][4]] if i])
            vote_list.append((rep_vote, rep_name))

        unix_time = self._get_unix_time(year, date_list[0][1])
        # TODO: Give votes a proper title
        return (unix_time,
                num_list[0][1],
                "foo",
                [x[1] for x in vote_list],
                [x[0] for x in vote_list]
                )

    def _get_page_from_blob(self, blob):
        fileReader = PyPDF2.PdfFileReader(io.BytesIO(blob))
        page_content = fileReader.getPage(0).extractText()
        page_content = page_content.replace('\n', '')
        page_content += '\n'
        return page_content

    def _get_unix_time(self, year, date):
        dt = datetime.datetime(int(year), int(date.split('/')[0]), int(date.split('/')[1]))
        unix_time = time.mktime(dt.timetuple())
        return unix_time


