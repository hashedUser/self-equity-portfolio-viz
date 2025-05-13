import os
import json
import requests
import pandas as pd

# Get all symbols available at AlphaVantage
symbol = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=ltts&apikey=ZZZZZZZZZZZZ'

# Main URL for getting stock price according to the symbol
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=LTTS.BSE&apikey=4EUVO2NPPLPDATD5'
r = requests.get(url)
data = r.json()

# Storing the fetched data to a json file
json_object = json.dumps(data)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

# Next Updates: Generalized pipeline to convert the fetched data and store it into a database
