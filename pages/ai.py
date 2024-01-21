import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os


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



genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')


def load_data():
    profit_url = "https://docs.google.com/spreadsheets/d/1UE5DtWPO3Px3B5fBhHwComSErSoHutHrxi9HdrodQIM/export?format=csv&gid=0"
    loss_url = "https://docs.google.com/spreadsheets/d/1UE5DtWPO3Px3B5fBhHwComSErSoHutHrxi9HdrodQIM/export?format=csv&gid=1187568754"

    try:
        profit_df = pd.read_csv(profit_url)
        loss_df = pd.read_csv(loss_url)

        st.success("Data read successfully.")
        return profit_df, loss_df
    except Exception as e:
        st.error(f"Error reading CSV data from Google Spreadsheet: {e}")
        st.stop()

    
    
    
def main():
    st.title('aiAnandSrinivasan')

    profit_df, loss_df = load_data()

    #Pie Chart for Profit
    fig1 = px.pie(profit_df, values="Amount", names="Categories", title="Profit", hole=0.4)
    st.plotly_chart(fig1)

    #Pie Chart for Loss
    fig2 = px.pie(loss_df, values="Amount", names="Categories", title="Loss", hole=0.4)
    st.plotly_chart(fig2)
    response = model.generate_content(" read the following data and provide valuable insights, both positive and negative, first table is profit/gains/salary, second table is spendings" + str(load_data()) )
    print(str(load_data()))
    print(response.text)
    st.write(response.text)
if __name__ == "__main__":
    main()