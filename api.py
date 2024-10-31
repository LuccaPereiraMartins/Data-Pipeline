from fastapi import FastAPI
from logging_config import logger
import pipeline_offline
import pandas as pd
import requests
import base64


'''
Work on an API to display df_all, or test.csv
First time learning about and working with APIs

GitHub Pages is a static hosting service, only supports static files
Consider GitHub's REST API to push data to a repo (i.e. the readme that is then displayed on Pages)
Looks v tricky
'''




# Final try




# CONSTANTS
GITHUB_TOKEN = '###'
REPO_OWNER = 'LuccaPereiraMartins'
REPO_NAME = 'Data-Pipeline'
README_FILE = 'README.md'
NEW_CONTENT = f'Updated README\n\n{data_specific_json}'

api_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{README_FILE}'

response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
response_data = response.json()




# Second try




# retrieve data from processed folder
data = pd.read_csv('processed/test.csv', index_col='ticker')

# could access a particular instrument and field instead
instrument = 'TESLA INC'
field = ['date','price']

data_specific = data.loc[instrument,field]
data_specific_json = data_specific.to_dict()

# GitHub pages URL
url = 'https://luccapereiramartins.github.io/Data-Pipeline/'

# Make a POST request to upload
response = requests.post(url, json=data_specific_json)

# Check response
if response.status_code == 200:
    logger.info('Upload successful')
else:
    logger.warn('Upload unsuccessful')



'''

initial try

# create an instance of FastAPI class
app = FastAPI()

# route decorator creating endpoint for HTTP GET requests
# at the url path /get-message
# define asynchronous function read() linked to decorator
@app.get("/get-message")
async def read(data_specific: pd.DataFrame):
    return 'test'

'''