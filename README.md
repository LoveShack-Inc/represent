# Represent

A project to bring greater awareness to state government representatives' voting activity. The end goal a mobile app that will send users push notifications such as "[Your representative] just voted YES on Bill [XXXX]. Tap for more info." The notification can then bring users to the app to read more about the bill, or they can swipe it away if they don't need more information. The first iteration of the project will likely be an email list instead of a mobile app as a proof-of-concept.

The idea is that people aren't currently represented by their elected representatives, but they don't realize that, so they keep voting for them. Greater awareness of a representative's voting record will help people find representatives who actually...represent them.

# Usage

This project uses a Python 3.7.x environment.

In the command line, run
```terminal
python3 -m venv ./env
source ./env/bin/activate
pip3 install -e .

# run the below to see run options
repp --help

# when you're done, exit the venv with
deactivate
```

Right now, the bulk of the program is in main.py.

# Data Source

This is the bill tracking info for the Connecticut state legislature:

https://www.cga.ct.gov/asp/CGABillInfo/CGABillInfoRequest.asp

You can find all bills on record ("All selected" under the "Choose One or More Session Year(s)" dropdown) but this seems to overload the site, and the page takes a few minutes to load, so maybe we should just limit our search to 2020.

I imagine this is the page that gets updated every time a new bill gets voted on.
