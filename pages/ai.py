import streamlit as st
import pandas as pd
import plotly.express as px

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
    fig1 = px.pie(profit_df, values="Amount", names="Category", title="Profit", hole=0.4)
    st.plotly_chart(fig1)

    #Pie Chart for Loss
    fig2 = px.pie(loss_df, values="Amount", names="Category", title="Loss", hole=0.4)
    st.plotly_chart(fig2)

if __name__ == "__main__":
    main()
