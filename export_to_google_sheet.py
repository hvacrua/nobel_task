from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
from getting_data import df  # import variable with data from site


# change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1lydZBvPRRstN1sFZkacbqZY30Vs_cEUAcFzUQWQ_80Y'

# change the range if needed
SAMPLE_RANGE_NAME = 'A1:AA1000'


def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    # print(SCOPES)

    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret_375823794938-voiuv7v2fd8af6gij7d8cmci5bekq6ga.apps.googleusercontent.com.json', SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        # return service
    except Exception as e:
        print(e)
        # return None


# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('client_secret_375823794938-voiuv7v2fd8af6gij7d8cmci5bekq6ga.apps.googleusercontent.com.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])


def export_data_to_sheets():
    response_date = service.spreadsheets().values().update(
        spreadsheetId = SAMPLE_SPREADSHEET_ID_input,
        valueInputOption = 'RAW',
        range = SAMPLE_RANGE_NAME,
        body = dict(majorDimension = 'ROWS',
                  values = df.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated')


def set_sheet_format():
    """Set format for sheet"""
    sheetId = 0
    results = service.spreadsheets().batchUpdate(
        spreadsheetId = SAMPLE_SPREADSHEET_ID_input,
        body = {"requests": [
            {"repeatCell": {"cell": {"userEnteredFormat":
                {"horizontalAlignment": 'CENTER',
                 "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8, "alpha": 1},
                 "textFormat": {"bold": True, "fontSize": 12}}
                                     },
                             "range": {"sheetId": sheetId,
                                       "startRowIndex": 0,
                                       "endRowIndex": 1,
                                       "startColumnIndex": 0,
                                       "endColumnIndex": df.shape[1]},
                             "fields": "userEnteredFormat"
                            }
            },
            {'updateBorders': {'range': {'sheetId': sheetId,
                                         'startRowIndex': 0,
                                         'endRowIndex': df.shape[0] + 1,
                                         'startColumnIndex': 0,
                                         'endColumnIndex': df.shape[1]},
                               # set style for bottom border
                               'bottom': {'style': 'SOLID',
                                          'width': 1,
                                          'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                               # set style for top border
                               'top': {'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                               # set style for left border
                               'left': {'style': 'SOLID',
                                        'width': 1,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                               # set style for right border
                               'right': {'style': 'SOLID',
                                         'width': 1,
                                         'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                               # set style for internal horizontal lines
                               'innerHorizontal': {'style': 'SOLID',
                                                   'width': 1,
                                                   'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                               # set style for internal vertical lines
                               'innerVertical': {'style': 'SOLID',
                                                 'width': 1,
                                                 'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}
                               }}
        ]
        }).execute()


export_data_to_sheets()
set_sheet_format()