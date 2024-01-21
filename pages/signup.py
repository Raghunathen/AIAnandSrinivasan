import streamlit as st
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title('Signup to aiAS')

loginid = st.text_input("Enter a userid")
password = st.text_input("Enter a password", type="password")

def create(title, credentials_file='credentials.json'):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build("sheets", "v4", credentials=credentials)
        
        spreadsheet = {"properties": {"title": title}}
        spreadsheet = (
            service.spreadsheets()
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )
        
        print(f"Spreadsheet ID: {spreadsheet.get('spreadsheetId')}")
        return spreadsheet.get("spreadsheetId")
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
a = st.button("Signup")
def append_to_spreadsheet(spreadsheet_id, sheet_name, column, values):
    # Load the credentials from the JSON file obtained from the Google API Console
    credentials_file = 'credentials.json'  # Replace with the path to your credentials file
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    
    # Build the Google Sheets API service
    service = build('sheets', 'v4', credentials=credentials)

    # Get the last row in the sheet to determine where to append the new data
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f'{sheet_name}!{column}:{column}').execute()
    values_in_sheet = result.get('values', [])
    
    if values_in_sheet:
        last_row = len(values_in_sheet) + 1
    else:
        last_row = 1

    # Append the new values after the last row in the specified column
    range_name = f'{sheet_name}!{column}{last_row}:{column}{last_row + len(values) - 1}'
    
    # Update the spreadsheet with the new values
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        body={'values': values},
        valueInputOption='RAW'
    )
    response = request.execute()
    
    print('Appended values successfully.')

if a:
    append_to_spreadsheet("1Hl61oMqfl0GX-Jrl0_VSV4hROVPJMmFl0UAmQns9L50", 'Sheet1', "A", [[loginid]])
    append_to_spreadsheet("1Hl61oMqfl0GX-Jrl0_VSV4hROVPJMmFl0UAmQns9L50", 'Sheet1', "B", [[password]])
    append_to_spreadsheet("1Hl61oMqfl0GX-Jrl0_VSV4hROVPJMmFl0UAmQns9L50", 'Sheet1', "C", [[create(loginid)]])
    st.write("Signed up, redirecting to login..")
    time.sleep(1)
    st.switch_page('main.py')