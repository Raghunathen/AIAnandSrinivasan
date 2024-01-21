import streamlit as st
import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account

def find_row_by_value(spreadsheet_id, sheet_name, column, target_value, credentials_file='credentials.json'):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build("sheets", "v4", credentials=credentials)

        # Read all values in the specified column
        range_name = f'{sheet_name}!{column}:{column}'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])

        if not values:
            print(f"No values found in column {column}.")
            return None

        # Search for the target value and return the row number
        for i, row in enumerate(values, start=1):
            if row and row[0] == target_value:
                return i

        print(f"Target value '{target_value}' not found in column {column}.")
        return None
    except Exception as error:
        print(f"An error occurred: {error}")
        return None



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
def get_value_at_cell(spreadsheet_id, sheet_name, row, column, credentials_file='credentials.json'):
    """
    Gets the value at a given row and column in a Google Sheets spreadsheet.
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build("sheets", "v4", credentials=credentials)

        # Read the value at the specified cell
        range_name = f'{sheet_name}!{column}{row}'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        value = result.get('values', [])

        if not value:
            print(f"No value found at cell {column}{row}.")
            return None

        return value[0][0]
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

st.title('Login to aiAnandSrinivasan')

#dd/mm/yyyy


loginid = st.text_input("Enter a userid")
password = st.text_input("Enter a password", type="password")



col1, col2 = st.columns([1,1])

with col1:
    a = st.button("Login")
with col2:
    b = st.button("Signup")

spreadsheet_id = '1Hl61oMqfl0GX-Jrl0_VSV4hROVPJMmFl0UAmQns9L50'
sheet_name = 'Sheet1'
column = 'A' 



if a:
    row_number = find_row_by_value(spreadsheet_id, sheet_name, column, loginid)
    if row_number is not None:
        pw = get_value_at_cell(spreadsheet_id, sheet_name, row_number, "B")
        if pw == password:
            st.session_state['userid'] = loginid
            st.session_state['person_url'] = get_value_at_cell(spreadsheet_id, sheet_name, row_number, "C")
            st.switch_page("pages/expense.py")
        else:
            st.toast("Wrong Password")
    else:
        st.toast("username doesnt exist, signup")
        print("Target value not found in the specified column.")
if b:
    st.switch_page("pages/signup.py")