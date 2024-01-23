import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Raw Data", initial_sidebar_state="collapsed")
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

col1, col2 = st.columns([1, 0.13])
st.title('Raw Earnings and Spendings Data')
with col1:
    a = st.button("Home")
with col2:
    b = st.button("Logout")
    
if a:
    st.switch_page('pages/dashboard.py')
if b:
    st.switch_page('main.py')     

def load_profit_data(credentials_file='credentials.json'):
    try:
        # Load Google Sheets API credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Build the Google Sheets API service
        service = build('sheets', 'v4', credentials=credentials)

        # Define the spreadsheet ID using session_state
        spreadsheet_id = st.session_state['person_url']

        # Define the range for the profit sheet
        profit_range = 'profit!A1:B1000'  # Adjust the range as needed

        # Get data from the profit sheet
        profit_result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=profit_range
        ).execute()
        profit_data = profit_result.get('values', [])

        st.success("Profit data read successfully.")
        return profit_data
    except Exception as e:
        st.error(f"Error reading profit data from Google Spreadsheet: {e}")
        st.stop()

def load_loss_data(credentials_file='credentials.json'):
    try:
        # Load Google Sheets API credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Build the Google Sheets API service
        service = build('sheets', 'v4', credentials=credentials)

        # Define the spreadsheet ID using session_state
        spreadsheet_id = st.session_state['person_url']

        # Define the range for the loss sheet
        loss_range = 'loss!A1:C1000'  # Adjust the range as needed

        # Get data from the loss sheet
        loss_result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=loss_range
        ).execute()
        loss_data = loss_result.get('values', [])

        st.success("Loss data read successfully.")
        return loss_data
    except Exception as e:
        st.error(f"Error reading loss data from Google Spreadsheet: {e}")
        st.stop()

def main():
    
    
    profit_data = load_profit_data()
    loss_data = load_loss_data()

    # Display the profit data in a table
    st.subheader('Profit Data')
    profit_column_names = ["Amount", "Date"]
    profit_df = pd.DataFrame(profit_data, columns=profit_column_names)
    profit_df.index += 1 
    st.table(profit_df)

    # Display the loss data in a table
    st.subheader('Loss Data')
    loss_column_names = ["Amount", "Date", "Category"]
    loss_df = pd.DataFrame(loss_data, columns=loss_column_names)
    loss_df.index += 1 
    st.table(loss_df)

if __name__ == "__main__":
    main()
