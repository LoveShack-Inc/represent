import requests
import logging
from bs4 import BeautifulSoup

CT_GOV_BASE_URI = "https://www.cga.ct.gov"
CT_GOV_STATUS = "/asp/cgabillstatus/cgabillstatus.asp"
CT_GOV_SEARCH = "/asp/CGABillInfo/CGABillInfoDisplay.asp"

CT_GOV_SEARCH_BASE_URI = f"{CT_GOV_BASE_URI}{CT_GOV_SEARCH}"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crawler")

def _ct_gov_search(year):
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
        CT_GOV_SEARCH_BASE_URI, 
        data=data, 
        headers=headers, 
        verify=False,
        timeout=60
    )
    response.raise_for_status()
    return response


def _get_soup_from_response(response):
    return BeautifulSoup(response.text, 'html.parser')


def _get_hrefs_from_soup(soup):
    hrefs = []
    for i in soup.find_all('a'):
        href = i.get('href')
        if href:
            hrefs.append(href)
    
    return hrefs


def _get_bill_pdf_links(relative_link):
    logger.info(f"Getting {relative_link}")
    response = requests.request(
        "GET", 
        f"{CT_GOV_BASE_URI}{relative_link}", 
        verify=False,
        timeout=30
    )
    response.raise_for_status()
    soup = _get_soup_from_response(response)
    hrefs = _get_hrefs_from_soup(soup)
    return_links = [i for i in hrefs if i.lower().endswith("pdf")]
    logging.info(f"Got {len(return_links)} from {relative_link}")

    return return_links


def get_relative_bill_links():
    start_year = 2020
    end_year = 2020

    bills_relative_links = set()
    for i in range(start_year, end_year + 1):
        logger.info(f"Searching for bills in year: {i}")
        r = _ct_gov_search(i)
        soup = _get_soup_from_response(r)
        bills_relative_links.update(
            set(x for x in _get_hrefs_from_soup(soup) if x.startswith(CT_GOV_STATUS))
        )
    
    return bills_relative_links


if __name__ == '__main__':
    pdf_links = set()
    relative_links = get_relative_bill_links()
    for i in relative_links:
        logging.info(i)
    for num, i in enumerate(relative_links):
        logger.info(f"{num}/{len(relative_links)} - Getting PDF links from: {i}")
        try:
            single_bill_pdf_links = _get_bill_pdf_links(i)
            single_bill_pdf_links = [CT_GOV_BASE_URI + i for i in single_bill_pdf_links]
            pdf_links.update(single_bill_pdf_links)
        except Exception as e: # idk what the requests exception is
            logging.exception("An exception ocurred when getting the pdf links")

    # This takes somewhere in the neighborhood of ten minutes to run for a single year.
    # It returns a set 'pdf_links' of unique PDF links that we'll need to pass to the parser.
