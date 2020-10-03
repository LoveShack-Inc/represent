import io
import PyPDF2
import re
import sys
import logging

from .BaseProcessor import BaseProcessor

class CtGovPdfProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()

        self.YAY_OR_NAY_PATTERN = re.compile(r"( Y | N )(.*?)(?= Y | N | \n)")
        self.DATE_PATTERN = r"(Taken on )(.*?)( )"
        self.VOTE_FOR_PATTERN = r"(Vote for )(.*?)( Seq)"
        self.UNKOWN_PATTERN = r"[a-zA-Z .]"

    def process_blob(self, blob):
        page_content = self._get_page_from_blob(blob)

        votes = re.findall(self.YAY_OR_NAY_PATTERN, page_content)
        date_list = re.findall(self.DATE_PATTERN, page_content)
        num_list = re.findall(self.VOTE_FOR_PATTERN, page_content)

        vote_list = []
        for i in range(len(votes)):
            t1 = votes[i][0]
            t2 = "".join(re.findall(self.UNKOWN_PATTERN, votes[i][1])).strip()
            vote_list.append((t1, t2))

        self._write_to_csv(
            2020, 
            date_list[0][1].replace("/", "_"),
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


    def _write_to_csv(self, year, date, bill_number, vote_name, rep_name, rep_vote):
        for num, val in enumerate(rep_vote):
            logging.info(f"""
                Year: {year}, Date: {date}, Bill Number: {bill_number}, Vote Name: {vote_name}
                Rep Name: {rep_name[num]}, Rep Vote: {rep_vote[num]}""")
