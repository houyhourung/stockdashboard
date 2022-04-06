import streamlit as st #Streamlit Application
import yfinance as yf #Yahoo Finance API
import requests
import config

#Changes the Favicon and Tab Title
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)
#Streamlit SideBar Navigation
st.sidebar.subheader("Stock Dashboard")

#Input from the user in order to get a Stock
stock_ticker=  st.sidebar.text_input("Enter a valid stock ticker....AAPL")
api_token= config.stockData_api_key
stockYahoo = yf.Ticker(stock_ticker)

# This gives an overview of the company - Information Box Widget
def information():
    information_block = st.sidebar.checkbox("See an Overview of the Company")
    if information_block:
        st.info(stockYahoo.info['longBusinessSummary'])
    pass

# Map class
def map():
    headquarter_map = st.sidebar.checkbox("See the Company's Headquarter")
    if headquarter_map:
        #Getting address from YahooFinance API
        address = (stockYahoo.info['address1'], stockYahoo.info['city'],stockYahoo.info['state'])
        #Import geopy and geolocator
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="stock dashboard")
        #Getting logitude and latitude from adress 
        data = geolocator.geocode(address)
        #Checking to see if either longitude or latidue is empty
        if not data.longitude or not data.latitude:
            st.error("We encoutered an error displaying the map. We apologize for any inconveniences this might cause.")
        else:
            latitude= data.latitude
            longitude= data.longitude
            map_creator(latitude, longitude)
    pass

def map_creator(latitude,longitude):
    from streamlit_folium import folium_static
    import folium
    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

if stock_ticker:
    parameters = {
    "symbols": stock_ticker,
    "api_token": api_token
    }
    stockData_url= "https://api.stockdata.org/v1/data/quote?"
    stockData= requests.get(stockData_url, params=parameters).json()
    st.title(stockData["data"][0]["name"] + "'s Dashboard")
    #st.write(stockData)
    information()
    st.header(stockData["data"][0]["name"] + "'s Headquarter")
    map()
else:
    st.warning("Please input a Stock's ticker")
