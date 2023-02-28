import data_pipeline as d_pipeline
from secedgar import FilingType
import pandas as pd
import time as t

test = True


#### OFFICIAL API ####
# @arg companies is a list of strings, where each element in the list is a
#   a ticker for a company
####
# Returns a dictionary/map of "ticker" : dataframe
def get_CSV_Filing4(companies: list[str]):
    dictionary = {}

    for company in companies:
        XML = d_pipeline.get_filings_XML(company)
        dataFrame = pd.DataFrame()
        for x in XML:
            df = d_pipeline.XML_CSV_Filing4(x)
            dataFrame = pd.concat([dataFrame, df], ignore_index=True)
        dictionary[company] = dataFrame

        # Needed to prevent Querying the EDGAR database too frequently and
        # causing a lockout from API
        t.sleep(.5)

    return dictionary


if __name__ == "__main__":
    dictionary = get_CSV_Filing4(["AMD", "AAPL", "GOOGL"])
    for x in dictionary:
        print(dictionary[x])
    # print(dictionary)


