running for the first time, make sure you:
	pip install -r requirements.txt
to install dependencies. Feel free to add to requirements.txt if needed

To run unit tests, in the terminal in venv directory:
	python test.py
	python3 test.py

test.py contains unit tests to try out, keep adding unit tests if needed


info, so far, data_pipeline.py contains the following functions:

	SaveFilings(company,  filingType = FilingType.FILING_4, user_agent='QuantProj (Dumb@usc.edu)', no_filings=3)

		company = string containing company ticker or name

		filingType = which form to find, by default gets form 4, 
			pass FilingType.FILING_<which filing>, 
			options at https://sec-edgar.github.io/sec-edgar/filingtypes.html

		user_agent = replace with '<name> (<email>)' 
			*Necessary for secedgar access

		no_filings = number of filings to retrieve, 
			by default gets 3 filings

		*Overview = Retrieves filings and stores them under 
			<program working directory>/filings/<company>/<form>
			*usually in XML format



