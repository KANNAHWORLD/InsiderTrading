import os
import requests
from secedgar import CompanyFilings, FilingType
from html.parser import HTMLParser
from lxml import etree
import pandas as pd

#### Needed for testing
# import xml.dom.minidom

# this is needed to get the data
# pip install secedgar
# docs https://sec-edgar.github.io/sec-edgar/filings.html#secedgar.CompanyFilings

# define transaction code variable from https://www.sec.gov/about/forms/form4data.pdf page 5

#TODO: List INCOMPLETE, also tried to summarize the ones I understood
#TODO: should we worry about runtime? idk if there are faster python data structures
txnCodeDescriptions = {
"P": "Purchase (open market or private)",
"S": "Sale (open market or private)",
"V": "Voluntarily reported earlier than required",   
"A": "Grant/award",
"D": "Sale (back to company)",
"F": "Payment of exercise price or tax liability using portion of securities received from the company",
"I": "Acquisition/disposion of issuer securities",
"M": "Exercise/conversion of derivative",
"C": "Conversion of derivative",
"E": "Expiration of short derivative",
"H": "Expiration of long derivative",
"O": "Exercise of out-of-the-money derivative",
"X" : "Exercise of in-the-money or at-the-money derivative security",
"K": "Equity swap/hedging txn"
}

#TODO - possible that it's not just one character - could be "S/K" - handle that

##########
# @arg xmlList is a list of etree objects containing XML
##########
# Returns a Pandas dataframe which can be use later to convert to CSV
def XML_CSV_Filing4(xmlList):
    #Building a 2d array
    rows = []

    for root in xmlList:
        ticker = root.find('issuer/issuerTradingSymbol').text
        name = root.find('reportingOwner/reportingOwnerId/rptOwnerName').text
        title = root.find('reportingOwner/reportingOwnerRelationship/officerTitle').text
        isDirector = root.find('reportingOwner/reportingOwnerRelationship/isDirector').text
        isOfficer = root.find('reportingOwner/reportingOwnerRelationship/isOfficer').text
        isTenPercentOwner = root.find('reportingOwner/reportingOwnerRelationship/isTenPercentOwner').text

        personalInfo = [name, title, isDirector, isOfficer, isTenPercentOwner]

        for transaction in root.findall('nonDerivativeTable/nonDerivativeTransaction'):
            row = getFieldsFromTxn(transaction, personalInfo)
            rows.append(row)

        for transaction in root.findall('derivativeTable/derivativeTransaction'):
            row = getFieldsFromTxn(transaction, personalInfo)
            rows.append(row)
    

    df = pd.DataFrame(rows, columns = ['Name', 'Title', 'isDirector', 'isOfficer', 'isTenPercentOwner', 'Security Type', 'Txn Type', 'Txn Date', 'Num Shares', 'Price'])
    df.index.name = "Row #"
    
    # save as a CSV
    os.makedirs('data', exist_ok=True)  
    df.to_csv('data/'+ ticker + '.csv')  
    # print(df)
    return df

##########
# @arg transaction is the xml node for each transaction
# @arg personalInfo is list of information about filing person - name, title, isDirector, isOfficer, isTenPercentOwner
##########
# Returns a list of transaction information to be used as a row in a dataframe
def getFieldsFromTxn(transaction, personalInfo):
    securityTitle = transaction.find('securityTitle/value').text
    transactionDate = transaction.find('transactionDate/value').text
    numShares = transaction.find('transactionAmounts/transactionShares/value').text
    txnCode = transaction.find('transactionCoding/transactionCode').text

    ############### Error given for below
    #####  price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
    #####    AttributeError: 'NoneType' object has no attribute 'text'
    ### Some transactions possibly don't disclose share price?
    ### issue, placed it under try, catch for the time being ~Sid
    try:
        price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
    except:
        price = -1
    
    try: 
        txnType = txnCodeDescriptions[txnCode]
    except:
        # if "P/K" or "S/K"
        if(txnCode[0] == "P" or txnCode[0] == "S"): 
            txnType = txnCodeDescriptions[txnCode]
        else: 
            txnType = "Other"
        
    row = personalInfo + [securityTitle, txnType, transactionDate, numShares, price]

    return row

##########
# @arg company is just a company name
# @arg filingType must be FilingType filing, allowed options https://sec-edgar.github.io/sec-edgar/filingtypes.html
# @arg user_agent is default, but please change it to "<your name> (<email>)"
# @arg no_filings is the amount of filings to retrieve
##########
# Returns a list of XML objects which can be parsed
def get_filings_XML(company, filingType = FilingType.FILING_4, user_agent='QuantProj (Dumb@usc.edu)', no_filings=3):

    ##### Getting all of the URLS to query Edgar
    filings = CompanyFilings(cik_lookup=[company], filing_type=filingType, count=no_filings, user_agent=user_agent)
    urls = filings.get_urls()

    #### Getting ticker
    company_ticker = list(urls.keys())[0]
    xml_return_docs = []

    #### Header
    UAHeader = { "User-Agent": user_agent}

    #### Querying all of the links and obtaining all of the XML
    for x in urls[company_ticker]:

        #### Getting document from the EDGAR database
        response = requests.get(x, headers=UAHeader)
        array = response.text.split("\n")

        #### Skipping through the array until we find the XML section
        i = 1
        for line in array:

            #### Skipping useless information
            if not line.startswith('<XML>'):
                i += 1
                continue

            break

        #### This gets the useful XML data to be later parsed
        html = ''
        while True:
            if array[i].startswith('</XML>'):
                break
            html += array[i]
            html += '\n'
            i += 1

        ############# For printing the XML generated during dev
        # append XML document to return array
        # temp = xml.dom.minidom.parseString(html)
        # new_xml = temp.toprettyxml()
        # print(new_xml)

        #### Adding all of the XML documents to the XML list
        root = etree.fromstring(html)
        xml_return_docs.append(root)

    # print(xml_return_docs)
    return xml_return_docs

#for testing - read from one file
def get_filings_from_file(XMLFileName):

    # Open the HTML file
    directory = os.getcwd()

    html = ''

    # This reads the XML file returned from EDGAR
    with open(directory + '/' + XMLFileName, 'r') as f:

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
    return [root]

if __name__ == "__main__":
    # xmlList = get_filings_from_file("filings/AMD/4/0000002488-23-000032.txt")
    xmlList = get_filings_XML("AAPL",no_filings=30)
    df = XML_CSV_Filing4(xmlList)

