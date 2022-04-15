# City of Seattle Number of 911 Calls Analysis
Before running any files, ensure to download the two necessary csv files.
The data for 911 calls can be found [here](https://data.seattle.gov/Public-Safety/Total-number-of-Fire-911-calls-per-day/umiy-nixb).
Simply go to export, and then download the CSV.
The data for COVID cases can be found [here](https://kingcounty.gov/depts/health/covid-19/data/summary-dashboard.aspx).
Scroll down to "Download COVID-19 data files" then download daily counts by city. This returns an Excel sheet.
To get the CSV, click on the Positives table of the Excel, then Save As a CSV.
Also ensure that the correct file paths for these CSV's are put into 'main.py.'
'data_load.py' must be in the same location as 'main.py' so that main.py can correctly call data_load functions
Depending on your environment, be sure to install the necessary packages seen at the top of 'main.py.'
Once that is complete, run 'main.py' to generate results.
