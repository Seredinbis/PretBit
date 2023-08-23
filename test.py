import pandas as pd
import apiclient
import httplib2
import os
import json

from oauth2client.service_account import ServiceAccountCredentials
from config_data.config import load_config

abspath = os.path.abspath('.env')
config = load_config(abspath)
json_token: dict = config.google_sheets_api.token
google_sheets_token = json.loads(json_token)
spreadsheet_ID = '1iw2mz3md74UeCIMy3eXnfBH-E2-rhwBkWosxwVZVJxM'
credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_token,
                                                               ["https://www.googleapis.com/auth/spreadsheets",
                                                                "https://www.googleapis.com/auth/drive"])
httpauth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpauth)
spreadsheet_info = service.spreadsheets().get(spreadsheetId=spreadsheet_ID, ranges="Июль'23 ").execute()

# data = pd.json_normalize(spreadsheet_info)
# a = data.to_csv('out.csv')
# data = pd.read_csv('out.csv')
# print(data['properties.sheetId'])
sheet_name = "Июль'23 "


