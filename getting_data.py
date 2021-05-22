# account-pavlo@nobel-automation.iam.gserviceaccount.com
import requests
import pandas as pd

code_of_countries = ['BGD', 'AUS', 'MNG', 'TGO', 'ZWE', 'KWT', 'CUB', 'JOR', 'PER', 'HKG']
countries = []
capitals = []

for c in code_of_countries:
    res = requests.get('https://restcountries.eu/rest/v2/alpha/' + c)
    countries.append(res.json()['name'])
    capitals.append(res.json()['capital'])

#print(f"List of countries: {countries}\nList of capitals: {capitals}")

dict_values = {"Country": countries, "Capital": capitals}

df = pd.DataFrame(dict_values)

#print(df)