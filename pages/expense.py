import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import datetime
def format_date(date):
    return date.strftime("%Y-%m-%d")

st.set_page_config(page_title="Record Data", initial_sidebar_state="collapsed")
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
st.title("Record Spendings")
with col1:
    a = st.button("Home")
with col2:
    b = st.button("Logout")
    
if a:
    st.switch_page('pages/dashboard.py')
if b:
    st.switch_page('main.py')     

def append_to_spreadsheet(spreadsheet_id, sheet_name, column, values):
    credentials_file = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)

    # Get the last row in the sheet to determine where to append the new data
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, 
        range=f'{sheet_name}!{column}:{column}'
    ).execute()
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


def main():
    
    st.write("wait till you get submitted notification, before submitting another")
    

    st.markdown(
        """
        <style>
        .btn-insights {
            display: block;
            margin: 0 auto;
            padding: 10px 20px;
            font-size: 20px;
            text-align: center;
            background-color: 
            color: 
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader("Profit")
    profit_amount = st.text_input("How much:", value=0, key="profit_amount")
    profit_date = st.date_input("Date:", key="profit_date")
    profit_submit_button = st.button("Submit Profit")

    
    st.subheader("Spendings")
    spending_amount = st.text_input("How much:", value=0, key="spending_amount")
    spending_date = st.date_input("Date:", key="spending_date")
    spending_category = st.selectbox("Category:", [
        "Food",
        "Essentials",
        "Shopping",
        "Rents/EMIs/Insurance",
        "Transportation",
        "Groceries",
        "Entertainment",
        "Savings/Investments",
        "Miscellaneous"
    ], key="spending_category")
    
    spending_submit_button = st.button("Submit Spending")

    if profit_submit_button:
        append_to_spreadsheet(st.session_state['person_url'], "profit", "A", [[profit_amount]])
        append_to_spreadsheet(st.session_state['person_url'], "profit", "B", [[format_date(profit_date)]])
        st.write("Profit Submitted:")
        st.write("Amount:", profit_amount)
        st.write("Date:", format_date(profit_date))
        
    if spending_submit_button:
        append_to_spreadsheet(st.session_state['person_url'], "loss", "A", [[spending_amount]])
        append_to_spreadsheet(st.session_state['person_url'], "loss", "B", [[format_date(spending_date)]])
        append_to_spreadsheet(st.session_state['person_url'], "loss", "C", [[spending_category]])
        st.write("Spending Submitted:")
        st.write("Amount:", spending_amount)
        st.write("Date:", format_date(spending_date))
        st.write("Category:", spending_category)

    insights_button = st.button("INSIGHTS", key="insights_button", help="Click for insights")
    if insights_button:
        st.switch_page('pages/ai.py')
    
if __name__ == "__main__":
    main()