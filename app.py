import streamlit as st #Streamlit Application
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
stock_ticker=  st.sidebar.text_input("Enter a valid stock ticker....GOOG")
api_token= config.stockData_api_key

# This gives an overview of the company - Information Box Widget
def information():
    information_block = st.sidebar.checkbox("See an Overview of the Company")
    if information_block:
        st.write(polyresponse)
        if polyresponse["status"] == "NOT_FOUND":
            st.error("No ticker found, please check input")
        else:
            description = polyresponse["results"]["description"]
            st.write(description)
    pass

# Map class
def map():
    headquarter_map = st.sidebar.checkbox("See the Company's Headquarter")
    if headquarter_map:
        if polyresponse["status"] == "OK":
            if 'address' in polyresponse["results"]:
                address1 = polyresponse["results"]["address"]["address1"], polyresponse["results"]["address"]["city"], \
                       polyresponse["results"]["address"]["state"]
                st.header(stockData["data"][0]["name"] + "'s Headquarter")
                #Import geopy and geolocator
                from geopy.geocoders import Nominatim

                geolocator = Nominatim(user_agent="stock dashboard")

                #Getting logitude and latitude from address
                data = geolocator.geocode(address1)

                #Checking to see if either longitude or latidue is empty
                if data == None:
                    st.error("There is no address avaliable")
                else:
                    latitude= data.latitude
                    longitude= data.longitude
                    map_creator(latitude, longitude)
            else: 
                st.error("There is no address avaliable")
            
        else:
            st.error("Please check the Ticker Symbol you have submitted and try again")

        
    pass

def map_creator(latitude,longitude):
    from streamlit_folium import folium_static
    import folium
    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    # add marker for the station
    folium.Marker([latitude, longitude], popup="HeadQuarters", tooltip="HeadQuarters").add_to(m)
    # call to render Folium map in Streamlit
    folium_static(m)

if stock_ticker:
    parameters = {
    "symbols": stock_ticker,
    "api_token": api_token
    }
    stockData_url= "https://api.stockdata.org/v1/data/quote?"
    stockData= requests.get(stockData_url, params=parameters).json()
    st.write(stockData)
    st.title(stockData["data"][0]["name"] + "'s Dashboard")
    polystocks_url = "https://api.polygon.io/v3/reference/tickers/{}?apiKey=WJtsWZ032pndm6sfV4BAUnbaoOL7ku6X".format(
        stock_ticker)
    # Polygon.io Response from API
    polyresponse = requests.get(polystocks_url).json()
    information()
    map()
else:
    st.warning("Please input a Stock's ticker")

# testing
