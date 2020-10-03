import logging
import requests
from .BaseCrawler import BaseCrawler
from rep.dao.VoteObjectDao import VoteObjectDao

class CtGovCrawler(BaseCrawler):
    def __init__(self):
        super()
        self.DEFAULT_TIMEOUT = 30
        self.voteObjectDao = VoteObjectDao()

    def crawl(self):
        logging.info("CtGovCrawler crawl")
        vote_object_urls = self._get_vote_object_download_urls()
        for i in vote_object_urls:
            vote_object = self._download_vote_object(i)
            self.voteObjectDao.write(vote_object, i)
    
    def _get_vote_object_download_urls(self):
        return [
            "https://cga.ct.gov/2020/VOTE/S/PDF/2020SV-00052-R00HB06004-SV.PDF"
        ]

    def _download_vote_object(self, url):
        req = requests.get(url, 
            stream=True, 
            timeout=self.DEFAULT_TIMEOUT,
            # FIXME: I get a cert error locally idk why, it's annoying
            verify=False
        )
        req.raise_for_status()
        return req.content
