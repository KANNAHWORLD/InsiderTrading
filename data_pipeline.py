import os
from secedgar import CompanyFilings, FilingType

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
