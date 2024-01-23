import streamlit as st

st.set_page_config(page_title="dashboard", initial_sidebar_state="collapsed")
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

def main():
    st.title("AiAnandSri")

    # Create a 2x2 grid layout for buttons
    col1, col2 = st.columns([1, 0.3])

    # Button to record expenses with improved styling
    if col1.button("Record Expenses", key="record_expenses_button", help="Click to record expenses"):
        st.switch_page("pages/expense.py")

    # Button for insights with improved styling
    if col2.button("Insights", key="insights_button", help="Click for insights"):
        st.switch_page("pages/ai.py")

    # Button for raw data with improved styling
    if col1.button("Raw Data", key="raw_data_button", help="Click to view raw data"):
        st.switch_page("pages/excel.py")
        

    # Button for logout with improved styling
    if col2.button("Logout", key="logout_button", help="Click to logout"):
        st.switch_page("main.py")
       

if __name__ == "__main__":
    main()
