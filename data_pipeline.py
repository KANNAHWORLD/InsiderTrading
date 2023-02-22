import os
from secedgar import CompanyFilings, FilingType
from html.parser import HTMLParser
from lxml import etree

# this is needed to get the data
# pip install secedgar
# docs https://sec-edgar.github.io/sec-edgar/filings.html#secedgar.CompanyFilings



# @arg company is just a company name
# @arg filingType must be FilingType filing, allowed options https://sec-edgar.github.io/sec-edgar/filingtypes.html
# @arg user_agent is default, but please change it to "<your name> (<email>)"
# @arg no_filings is the amount of filings to retrieve
# Queries the edgar database and saves onto computer file tree at this directory
#      <proogram working directory>/filings/<company name>/<files>
# creates the directory if it does not already exist
# Path is not hardcoded, it is transportable to other computers
def SaveFilings(company, filingType = FilingType.FILING_4, user_agent='QuantProj (Dumb@usc.edu)', no_filings=3):

    # Requesting from EDGAR
    filings = CompanyFilings(cik_lookup=[company], filing_type=filingType, count=no_filings, user_agent=user_agent)

    # Path at which to save file
    program_working_directory = os.getcwd()
    savePath = program_working_directory + "/filings/"
    # creating directory if it does not already exist
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Saving files to the directory
    filings.save(savePath)

    return True

data = []

def XML_to_CSV(XMLFileName):

    # Define a list to store the data

    # Open the HTML file
    directory = os.getcwd()

    html = ''

    # This reads the XML file returned from EDGAR
    with open(directory+"/filings/AMD/4/0000002488-23-000032.txt", 'r') as f:

        # This first loop gets rid of the headers which we do not need
        for line in f:
            # Skip lines until we reach the line we're looking for
            if not line.startswith('<XML>'):
                continue

            # Get rid of '<XML>' so we get to the actually useful stuff
            f.readline()
            break

        # This gets the useful XML data
        for line in f:
            if line.startswith('</XML>'):
                break
            html += line

    # Loading XML file into xml parser
    root = etree.fromstring(html)

    #Testing finding a specific element in the XML file
    tag_elem = root.find('reportingOwner/reportingOwnerId/rptOwnerCik')
    tag_text = tag_elem.text

    #Printing that shit out
    print(tag_text)  # Output: 'Some text'


if __name__ == "__main__":
    XML_to_CSV("filings/AMD/4/0000002488-23-000032.txt")

