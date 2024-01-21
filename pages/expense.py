import streamlit as st
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

def main():
    st.title("aiAnandSrinivasan")
    
    insights_button = st.button("INSIGHTS", key="insights_button", help="Click for insights")

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
        st.write("Profit Submitted:")
        st.write("Amount:", profit_amount)
        st.write("Date:", profit_date)
        
    if spending_submit_button:
        st.write("Spending Submitted:")
        st.write("Amount:", spending_amount)
        st.write("Date:", spending_date)
        st.write("Category:", spending_category)

    
if __name__ == "__main__":
    main()
