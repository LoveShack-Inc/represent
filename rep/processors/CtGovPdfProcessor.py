import io
import pdfplumber
import re
import sys
import logging
import datetime
import time

from .Exceptions import PdfProcessorException
from .BaseProcessor import BaseProcessor
from rep.dataclasses.ProcessedVoteResult import ProcessedVoteResult
from rep.dataclasses.VoteObject import VoteObject
from rep.dao.RepresentativeInfoDao import RepresentativeInfoDao


class CtGovPdfProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()

        self.YAY_OR_NAY_PATTERN = re.compile(r"\s(Y|N|A|X)\s(.+?)(?=\s+(Y|N|A|X)\s+|\\n|$)")
        self.DATE_PATTERN = r"(Taken on )(.*?)( )"
        self.VOTE_FOR_PATTERN = r"Vote for\W+([^\s]+)"
        self.NUM_PATTERN = re.compile(r"\d+")

        self.state = 'CT'

    def process_blob(self, vote_object: VoteObject) -> ProcessedVoteResult:
        try: 
            return self._process_blob_wrapper(vote_object)
        except Exception as e:
            raise PdfProcessorException("An exception occurred while processing a file")
    
    def _convert_rep_name_match_to_name(self, name_match: str):
        name_parts = []
        name_match = name_match.split()
        for i in name_match:
            if not self.NUM_PATTERN.match(i) and i != "VACANT":
                # big hack
                name_parts.append(i.upper())
        if len(name_parts) < 1:
            name_parts = ["UNKNOWN"]
        return (" ").join(name_parts)

    def _process_blob_wrapper(self, vote_object: VoteObject) -> ProcessedVoteResult:
        page_content = self._get_page_from_blob(vote_object.blob)

        votes = re.findall(self.YAY_OR_NAY_PATTERN, page_content)
        date_list = re.findall(self.DATE_PATTERN, page_content)
        num_list = re.findall(self.VOTE_FOR_PATTERN, page_content, re.IGNORECASE)
        year = vote_object.sourceUrl.split('/')[3]
        if len(votes) <= 1:
            raise PdfProcessorException("PDF file can't be read")

        vote_list = []
        for i in range(len(votes)):
            rep_vote = votes[i][0]
            rep_name = self._convert_rep_name_match_to_name(votes[i][1])
            vote_list.append((rep_vote, rep_name))

        unix_time = self._get_unix_time(year, date_list[0][1])

        representativeInfoDao = RepresentativeInfoDao()
        repIds = [representativeInfoDao.get_id_from_name(x[1]) for x in vote_list]


        # TODO: Give votes a proper title
        return ProcessedVoteResult(
            unixTime=unix_time, 
            billNumber=num_list[0],
            voteName=num_list[0],
            repId=repIds,
            repVote=[x[0] for x in vote_list],
            rawVoteObjectId=vote_object.vote_id
        )

    def _get_page_from_blob(self, blob):
        with pdfplumber.open(io.BytesIO(blob)) as pdf:
            return pdf.pages[0].extract_text().replace('\n', '')

    def _get_unix_time(self, year, date):
        dt = datetime.datetime(int(year), int(date.split('/')[0]), int(date.split('/')[1]))
        unix_time = time.mktime(dt.timetuple())
        return unix_time
