


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


#### Testing bullshit
if __name__ == "6__main__":
    name = "QuantSC"
    email = "usc@usc.edu"
    headers = { "User-Agent": f"{name} {email}"}
    # # cik = 0000320193
    # cik = "0000320193"
    # edgar_filings = requests.get(f"https://data.sec.gov/submissions/CIK{cik:0>10}.json", headers=headers).json()
    # print(edgar_filings.keys())
    # print(edgar_filings)


    # Specify the company CIK and date range
    cik = "0001720104" # "0000320193"
    start_date = "2022-01-01"
    end_date = "2022-01-31"

    # Define the API endpoint URL and parameters
    url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcurrent",
        "CIK": cik,
        "type": "4",
        # "dateb": end_date,
        "owner": "include",
        "start": "",
        "output": "atom",
        "count": "5",
    }

    # Send the HTTP request and get the response
    response = requests.get(url, params=params, headers=headers)

    # Print the response content
    root = etree.fromstring(response.content)
    # print(response.content)
    temp = xml.dom.minidom.parseString(response.content)
    new_xml = temp.toprettyxml()
    print(root)
    print(new_xml)

#### Testing bullshit
if __name__ == "6__main__":
    # # It needs the ticker symbol for this to work!
    # company = "AAPL"
    # filingType = FilingType.FILING_4
    # no_filings = 4
    # user_agent = 'QuantProj (Dumb@usc.edu)'
    # filings = CompanyFilings(cik_lookup=[company], filing_type=filingType, count=no_filings, user_agent=user_agent)
    # urls = filings.get_urls()
    # print(urls)
    # company = urls.keys()[0]
    # for x in urls[company]:
    #     print(x)
    #
    # name = "QuantSC"
    # email = "usc@usc.edu"
    # headers = { "User-Agent": f"{name} {email}"}
    #
    # response = requests.get(urls[company][0], headers=headers)
    #
    # print(response.content)
    # # Print the response content
    # root = etree.fromstring(response.content)
    # # print(response.content)
    # temp = xml.dom.minidom.parseString(response.content)
    # new_xml = temp.toprettyxml()
    # # print(root)
    # print(new_xml)
    #
    # # XML_to_CSV("filings/AMD/4/0000002488-23-000032.txt")
    array = " "
# array = get_filings_XML("AAPL")

######### Old version, with paths and Sarah's dataframe Code
def XML_to_CSV(XMLFileName):

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

    #Building a 2d array
    rows = []

    ticker = root.find('issuer/issuerTradingSymbol').text
    name = root.find('reportingOwner/reportingOwnerId/rptOwnerName').text

    for transaction in root.findall('nonDerivativeTable/nonDerivativeTransaction'):
        securityTitle = transaction.find('securityTitle/value').text
        transactionDate = transaction.find('transactionDate/value').text
        numShares = transaction.find('transactionAmounts/transactionShares/value').text
        price = transaction.find('transactionAmounts/transactionPricePerShare/value').text

        row = [ticker, name, securityTitle, transactionDate, numShares, price]
        rows.append(row)

    for transaction in root.findall('derivativeTable/derivativeTransaction'):
        securityTitle = transaction.find('securityTitle/value').text
        transactionDate = transaction.find('transactionDate/value').text
        numShares = transaction.find('transactionAmounts/transactionShares/value').text
        price = transaction.find('transactionAmounts/transactionPricePerShare/value').text

        row = [ticker, name, securityTitle, transactionDate, numShares, price]
        rows.append(row)

    df = pd.DataFrame(rows, columns = ['ticker', 'name', 'Security Type', 'Transaction Date', 'Num Shares', 'Price'])

    print(df.to_string())



############ Legacy testing teh functionality of the XML to csv and stuff
array = get_filings_XML("AAPL")
for x in array:
    # print (etree.tostring(array[0], pretty_print=True).decode())
    # print(x.find("issuer/issuerTradingSymbol").text)
    XML_to_CSV(x)
