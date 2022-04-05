import streamlit as st
import yfinance as yf
import requests
import config

#Changes the Favicon and Tab Title
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)
st.title("Stock Market Dashboard")

#Input from the user in order to get a Stock
stock_ticker= st.text_input("Enter a valid stock ticker....AAPL")
api_token= config.stockData_api_key
stockYahoo = yf.Ticker(stock_ticker)

if stock_ticker:
    parameters = {
    "symbols": stock_ticker,
    "api_token": api_token
    }
    stockData_url= "https://api.stockdata.org/v1/data/quote?"
    stockData= requests.get(stockData_url, params=parameters).json()

    st.write(stockData)
else:
    st.warning("Please input a Stock's ticker")

#There should be a new comment here in GitHub
information_block = st.checkbox("See an Overview of the Company")
if information_block:
    st.info(stockYahoo.info['longBusinessSummary'])

headquarter_map = st.checkbox("See the Company's Headquarter")
if headquarter_map:
    company_name = yf.Ticker(stock_ticker).info['longName']
    st.write(company_name)

#Introduction to the Map Class
def map_creator(latitude,longitude):
    from streamlit_folium import folium_static
    import folium
    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)


