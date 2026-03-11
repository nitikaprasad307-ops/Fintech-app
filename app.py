import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Financial Statement Analyzer", layout="wide")

st.title("📊 Financial Statement Analysis App")
st.write("Upload financial statement data to perform automated analysis.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Financial Data")
    st.dataframe(df)

    # Select company
    company = st.selectbox("Select Company", df["Company"].unique())

    company_df = df[df["Company"] == company]

    st.subheader(f"Financial Data for {company}")
    st.dataframe(company_df)

    st.subheader("📈 Revenue Trend")

    fig = px.line(company_df,
                  x="Year",
                  y="Revenue",
                  markers=True,
                  title="Revenue Growth")

    st.plotly_chart(fig, use_container_width=True)

    # Ratio Analysis
    st.subheader("📊 Ratio Analysis")

    company_df["Current Ratio"] = company_df["Current Assets"] / company_df["Current Liabilities"]

    company_df["Debt to Equity"] = company_df["Total Debt"] / company_df["Equity"]

    company_df["Net Profit Margin"] = company_df["Net Profit"] / company_df["Revenue"]

    st.dataframe(company_df[[
        "Year",
        "Current Ratio",
        "Debt to Equity",
        "Net Profit Margin"
    ]])

    # Profit Trend
    st.subheader("📉 Profit Trend")

    fig2 = px.bar(company_df,
                  x="Year",
                  y="Net Profit",
                  title="Net Profit Trend")

    st.plotly_chart(fig2, use_container_width=True)

    # Financial Health Score
    st.subheader("🧠 Financial Health Score")

    avg_margin = company_df["Net Profit Margin"].mean()
    avg_current = company_df["Current Ratio"].mean()
    avg_de = company_df["Debt to Equity"].mean()

    score = (avg_margin*40 + avg_current*30 + (1/avg_de)*30)*10

    score = min(score,100)

    st.metric("Financial Health Score", f"{round(score,2)} / 100")

    if score > 75:
        st.success("Company Financial Health: Strong")

    elif score > 50:
        st.warning("Company Financial Health: Moderate")

    else:
        st.error("Company Financial Health: Weak")

    # Company Comparison
    st.subheader("🏢 Company Comparison")

    avg_profit = df.groupby("Company")["Net Profit"].mean().reset_index()

    fig3 = px.bar(avg_profit,
                  x="Company",
                  y="Net Profit",
                  title="Average Profit Comparison")

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload a financial Excel file to begin analysis.")
