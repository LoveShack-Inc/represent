import logging
import requests
from .BaseCrawler import BaseCrawler
from rep.dataclasses.VoteObject import VoteObject
from rep.dataclasses.Enums import SourceType, SourceFormat
from rep.dao.VoteObjectDao import VoteObjectDao
from bs4 import BeautifulSoup

# TODO: fix the ssl errors eventually, for now though, the warning logs are a PITA
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CtGovCrawler(BaseCrawler):
    def __init__(self):
        super()
        self.DEFAULT_TIMEOUT = 60
        self.voteObjectDao = VoteObjectDao()
        self.CT_GOV_BASE_URI = "https://www.cga.ct.gov"
        self.CT_GOV_STATUS = "/asp/cgabillstatus/cgabillstatus.asp"
        self.CT_GOV_SEARCH = "/asp/CGABillInfo/CGABillInfoDisplay.asp"
        self.CT_GOV_SEARCH_BASE_URI = f"{self.CT_GOV_BASE_URI}{self.CT_GOV_SEARCH}"

    def crawl(self):
        logging.info("CtGovCrawler crawl")
        vote_object_urls = self._get_vote_object_download_urls()
        logging.info(f"Got {len(vote_object_urls)} to ingest")
        for num, i in enumerate(vote_object_urls):
            if self.voteObjectDao.isUrlIngested(i):
                logging.info(f"Skipping request for already ingested url {i}")
                continue
            try:
                logging.info(f"Get pdf {num}/{len(vote_object_urls)}")
                blob = self._download_vote_object(i)
            except requests.exceptions.HttpError as e:
                logging.exception("HTTPError caught when making request to resource server")
                continue

            # TODO: store the format and type ints in an enum
            vote_object = VoteObject(blob=blob, sourceUrl=i, sourceType=SourceType.CT_STATE_GOV.value, sourceFormat=SourceFormat.PDF.value)
            self.voteObjectDao.write(vote_object)

    def _ct_gov_search(self, year):
        data = {
            "cboComm": "X",
            "cboSessYr": year,
            "optCrit": "and",
            "optFindT": "crit",
            "selectItemcboSessYr": year
        }
        headers = {
            'origin': "https://www.cga.ct.gov",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }

        response = requests.request(
            "POST",
            self.CT_GOV_SEARCH_BASE_URI,
            data=data,
            headers=headers,
            verify=False,
            timeout=60
        )
        response.raise_for_status()
        return response

    def _get_soup_from_response(self, response):
        return BeautifulSoup(response.text, 'html.parser')

    def _get_hrefs_from_soup(self, soup):
        hrefs = []
        for i in soup.find_all('a'):
            href = i.get('href')
            if href:
                hrefs.append(href)

        return hrefs

    def get_relative_bill_links(self):
        start_year = 2011
        end_year = 2020

        bills_relative_links = set()
        for i in range(start_year, end_year + 1):
            logging.info(f"Searching for bills in year: {i}")
            r = self._ct_gov_search(i)
            soup = self._get_soup_from_response(r)
            bills_relative_links.update(
                set(x for x in self._get_hrefs_from_soup(soup) if x.startswith(self.CT_GOV_STATUS))
            )

        return bills_relative_links

    def _get_bill_pdf_links(self, relative_link):
        logging.info(f"Getting {relative_link}")
        response = requests.request(
            "GET",
            f"{self.CT_GOV_BASE_URI}{relative_link}",
            verify=False,
            timeout=30
        )
        response.raise_for_status()
        soup = self._get_soup_from_response(response)
        hrefs = self._get_hrefs_from_soup(soup)
        return_links = [i for i in hrefs if i.lower().endswith("pdf")]
        logging.info(f"Got {len(return_links)} from {relative_link}")

        return return_links

    def _get_vote_object_download_urls(self):
        pdf_links = set()
        relative_links = self.get_relative_bill_links()
        for num, i in enumerate(relative_links):
            logging.info(f"{num}/{len(relative_links)} - Getting PDF links from: {i}")
            try:
                single_bill_pdf_links = self._get_bill_pdf_links(i)
                single_bill_pdf_links = [self.CT_GOV_BASE_URI + i for i in single_bill_pdf_links]
                pdf_links.update(single_bill_pdf_links)
            except Exception as e:  # idk what the requests exception is
                logging.exception("An exception ocurred when getting the pdf links")
        return list(pdf_links)

    def _download_vote_object(self, url):
        req = requests.get(url, 
            stream=True, 
            timeout=self.DEFAULT_TIMEOUT,
            # FIXME: I get a cert error locally idk why, it's annoying
            verify=False
        )
        
        requestBlob = None
        if req.ok:
            requestBlob = req.content
        elif req.status_code == 404:
            logging.error(f"The resource server returned a 404 for the resouce:\n\t{url}")
        else:
            req.raise_for_status()
        return requestBlob
