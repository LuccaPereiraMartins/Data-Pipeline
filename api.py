from fastapi import FastAPI
import pipeline_offline
import pandas as pd


'''
Work on an API to display df_all, or test.csv
First time learning about and working with APIs
'''

# retrieve data from processed folder
data = pd.read_csv('processed/test.csv', index_col='ticker')

# could access a particular instrument and field instead

instrument = 'TESLA INC'
field = ['date','price']

data_specific = data.loc[instrument,field]

# create an instance of FastAPI class
app = FastAPI()

# route decorator creating endpoint for HTTP GET requests
# at the url path /get-message
# define asynchronous function read() linked to decorator
@app.get("/get-message")
async def read(data_specific: pd.DataFrame):
    return data_specific.to_csv()

