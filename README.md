# am-i-represented

A project to bring greater awareness to state government representatives' voting activity. The end goal a mobile app that will send users push notifications such as "[Your representative] just voted YES on Bill [XXXX]. Tap for more info." The notification can then bring users to the app to read more about the bill, or they can swipe it away if they don't need more information. The first iteration of the project will likely be an email list instead of a mobile app as a proof-of-concept.

The idea is that people aren't currently represented by their elected representatives, but they don't realize that, so they keep voting for them. Greater awareness of a representative's voting record will help people find representatives who actually...represent them.

# Usage

This project uses a Python 3.7.x environment.

In the command line, run
```terminal
pip install -r requirements.txt
```
Right now, the bulk of the program is in main.py.

# Data Source

This is the bill tracking info for the Connecticut state legislature:

https://www.cga.ct.gov/asp/CGABillInfo/CGABillInfoRequest.asp

You can find all bills on record ("All selected" under the "Choose One or More Session Year(s)" dropdown) but this seems to overload the site, and the page takes a few minutes to load, so maybe we should just limit our search to 2020.

I imagine this is the page that gets updated every time a new bill gets voted on.

# To-Do
- Web app front-end: should collect a user's email address and zip code
- Back-end: find state representatives from zip code. Starting with just Connecticut, then we'll expand as necessary
- Database: to store PDFs of each bill taken from the government website
- Web crawler: crawl the CT state government website ~once a day, and update the database
- Document parser: read PDF files and generate a CSV dataset of representative names and their votes. This dataset will be maintained in a separate public repo so the data is open and accessible
- Notification generator: whenever the dataset is updated, generate a notification for the relevant users and send it
