import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldometers.info/coronavirus")

soup = BeautifulSoup(page.content, 'lxml')
table = soup.find('table', attrs={'id': 'main_table_countries_today'})

rows = table.find_all("tr", attrs={"style": ""})

data = []
for i,item in enumerate(rows):
    
    if i == 0:
        
        data.append(item.text.strip().split("\n")[:13])
        
    else:
        data.append(item.text.strip().split("\n")[:12])

# to suppress future warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import dask.dataframe as dd

dt = pd.DataFrame(data)
dt = pd.DataFrame(data[1:], columns=data[0][:12]) #Formatting the header
df = dd.from_pandas(dt,npartitions=1)

df = df.drop(df.columns[[0]], axis=1)


df.to_csv('logstash/data_*.csv')