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

        for transaction in root.findall('nonDerivativeTable/nonDerivativeTransaction'):
            securityTitle = transaction.find('securityTitle/value').text
            transactionDate = transaction.find('transactionDate/value').text
            numShares = transaction.find('transactionAmounts/transactionShares/value').text


            ############### Error given for below
            #####  price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
            #####    AttributeError: 'NoneType' object has no attribute 'text'
            ### Some transactions possibly don't disclose share price?
            ### issue, placed it under try, catch for the time being ~Sid
            try:
                price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
            except:
                price = -1

            row = [ticker, name, securityTitle, transactionDate, numShares, price]
            rows.append(row)

        for transaction in root.findall('derivativeTable/derivativeTransaction'):
            securityTitle = transaction.find('securityTitle/value').text
            transactionDate = transaction.find('transactionDate/value').text
            numShares = transaction.find('transactionAmounts/transactionShares/value').text


            ############### Error given for below
            #####  price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
            #####    AttributeError: 'NoneType' object has no attribute 'text'
            ### Some transactions possibly don't disclose share price?
            ### issue, placed it under try, catch for the time being ~Sid
            try:
                price = transaction.find('transactionAmounts/transactionPricePerShare/value').text
            except:
                price = -1

        row = [ticker, name, securityTitle, transactionDate, numShares, price]
        rows.append(row)
    

    df = pd.DataFrame(rows, columns = ['ticker', 'name', 'Security Type', 'Transaction Date', 'Num Shares', 'Price'])
    # df.to_csv()
    print(df)
    return df



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


if __name__ == "__main__":
    xmlList = get_filings_XML("AAPL")
    df = XML_CSV_Filing4(xmlList)

