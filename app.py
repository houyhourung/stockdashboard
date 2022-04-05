import streamlit as st
import requests
import config

st.title("The Stock Market")

stock_ticker= st.text_input("Enter a valid stock tiker....AAPL")
api_token= config.stockData_api_key

if stock_ticker:
    parameters = {
    "symbols": stock_ticker,
    "api_token": api_token
    }
    stockData_url= "https://api.stockdata.org/v1/data/quote?"
    stockData= requests.get(stockData_url, params=parameters).json()

    st.write(stockData)
else:
    st.warning("empty value")



