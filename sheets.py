from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Union


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1NPcJBlrHbeRwSnDajfuZtBmbWqcb2aUEdXjpxPEy02A'


def get_cell_value(column_id: Union[str, int], row_id: Union[str, int]) -> list:
    creds = None

    # Если вход уже был, то повторная авторизация не нужна
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Если авторизации не было
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=f"Sheet1!{column_id}{row_id}").execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return []

        return values
    except HttpError as err:
        print(err)


def update_value(range_name: str, value_input_option: str, values: list):
    # Подразумевается, что авторизация уже была
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:

        service = build('sheets', 'v4', credentials=creds)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def find_cells_by_value(value: str) -> list:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    rows_with_value = list()
    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=f"Sheet1").execute()
        values = result.get('values', [])

        for user in values[1:]:
            if value in user:
                rows_with_value.append(user)

        if not values:
            print('No data found.')
            return []

        return rows_with_value
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    print(find_cells_by_value("1АA"))
    # print(get_cell_value("A", 1))
    # update_value("1NPcJBlrHbeRwSnDajfuZtBmbWqcb2aUEdXjpxPEy02A",
    #              "e1", "USER_ENTERED",
    #              [
    #                  ['A'],
    #              ])
