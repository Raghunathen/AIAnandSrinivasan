import streamlit as st
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time, json

st.set_page_config(page_title="Signup", initial_sidebar_state="collapsed")
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



def create(title, credentials_file=st.secrets['credentials']):
    credentials_dict = dict(credentials_file)
    credentials_json = json.loads(json.dumps(credentials_dict))
    try:
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build("sheets", "v4", credentials=credentials)

        # Create a new spreadsheet
        spreadsheet = {
            "properties": {"title": title},
            "sheets": [
                {"properties": {"title": "profit"}},
                {"properties": {"title": "loss"}}
            ]
        }
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

def append_to_spreadsheet(spreadsheet_id, sheet_name, column, values):
    # Load the credentials from the JSON file obtained from the Google API Console
    credentials_file=st.secrets['credentials']
    credentials_dict = dict(credentials_file)
    credentials_json = json.loads(json.dumps(credentials_dict))
    credentials = service_account.Credentials.from_service_account_info(credentials_json, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    
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

def is_value_in_column(spreadsheet_id, sheet_name, column_name, target_value):
    credentials_file=st.secrets['credentials']
    credentials_dict = dict(credentials_file)
    credentials_json = json.loads(json.dumps(credentials_dict))
    # Load Google Sheets API credentials
    credentials = service_account.Credentials.from_service_account_info(
        credentials_json,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    # Build the Google Sheets API service
    service = build('sheets', 'v4', credentials=credentials)

    # Define the range for the specified column
    range_name = f"{sheet_name}!{column_name}:{column_name}"

    try:
        # Get data from the specified column
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        values_in_column = result.get('values', [])

        # Check if the target value is in the specified column
        return [target_value] in values_in_column
    except Exception as e:
        print(f"Error reading data from Google Spreadsheet: {e}")
        return False

def is_password_standard(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True


st.title('Signup to aiAnandSri')
loginid = st.text_input("Enter a userid")
password = st.text_input("Enter a password", type="password")

# Signup button
if st.button("Signup"):
    if is_value_in_column(st.secrets["user_pass"], "Sheet1", "A", loginid):
        st.warning("Login ID EXISTS, Try a different one")
    else:
        if is_password_standard(password):
            # Perform signup actions
            append_to_spreadsheet(st.secrets["user_pass"], 'Sheet1', "A", [[loginid]])
            append_to_spreadsheet(st.secrets["user_pass"], 'Sheet1', "B", [[password]])
            append_to_spreadsheet(st.secrets["user_pass"], 'Sheet1', "C", [[create(loginid)]])

            # Display success message and perform redirect
            st.balloons()
            st.success("Signed up successfully!")
            st.info("Redirecting to login...")
            time.sleep(2)
            st.switch_page('main.py')
        else:
            st.warning("Password must be at least 8 characters long and contain at least one number.")