import numpy as np
import streamlit as st #Streamlit Application
import requests
import config
import pandas as pd
import csv

#Changes the Favicon and Tab Title
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

page = st.sidebar.selectbox("Choose your page", ["Home", "Stock Search"])

if page == "Home":
    # Display details of page 1
    #method to display interactive table
    def interactive_table():
        st.subheader("Popular Stocks in the Market")
        # Creates button so that users can choose what data they want to show onto the table
        parameters_table = st.multiselect(
            "Select one or more parameters to display in the interactive table",
            ["Low", "High", "Market cap", "Currency", "Volume"])

        # Line 96 is reading the CSV file with an updated file of the most popular stocks
        popular_stocks = pd.read_csv('Popular_Stocks2.csv')
        # Line 98 displays the data as a dataframe(interactive table)
        st.dataframe(popular_stocks[["Company", "Ticker symbol", "Price"] + parameters_table])

    # Bar graph compares popular stock prices
    def bar_graph():
        st.subheader("Popular Stocks in the Market (Price Comparison)")
        st.warning("Prices are not updated in real time.")
        # x_axis array is utilizing CSV file to import ticker symbols.
        x_axis = []
        with open('popular_stock_tickers.csv', newline='') as inputfile:
            for row in csv.reader(inputfile):
                x_axis.append(row[0])
        # y_axis array is utilizing CSV file to import stock prices.
        y_axis = []
        with open('popular_stock_prices.csv', newline='') as inputfile:
            for row in csv.reader(inputfile):
                y_axis.append(row[0])
        # Index is the list of ticker symbols (names)
        data = pd.DataFrame({
            'index': x_axis,
            'Stock Price (USD)': y_axis,
        }).set_index('index')
        # displaying bar-chart
        st.bar_chart(data)


    interactive_table()
    bar_graph()

elif page == "Stock Search":
  # This gives an overview of the company - Information Box Widget
    def information():
        information_block = st.sidebar.checkbox("See an Overview of the Company")
        name = stockData["data"][0]["name"]
        if information_block:

            if polyresponse["status"] == "NOT_FOUND":
                st.error("No ticker found, please check input")
            else:
                st.subheader(name + "'s Description")
                description = polyresponse["results"]["description"]
                st.write("\n\n")
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
                    st.subheader(stockData["data"][0]["name"] + "'s Headquarter")
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

    def price():
        col1, col2, col3 = st.columns(3)
        polystocks_url2 = "https://api.polygon.io/v2/aggs/ticker/{}/" \
                          "prev?adjusted=true&apiKey=WJtsWZ032pndm6sfV4BAUnbaoOL7ku6X".format(stock_ticker)
        polyresponse2 = requests.get(polystocks_url2).json()
        name = stockData["data"][0]["name"]
        st.subheader(name + "'s Previous Day Closing Information")

        if st.button('See Previous Closing Information'):
            if polyresponse2["status"] == "OK":
                closeprice = polyresponse2["results"][0]["c"]
                highestprice = polyresponse2["results"][0]["h"]
                lowestprice = polyresponse2["results"][0]["l"]
                openprice = polyresponse2["results"][0]["o"]
                ntrans = polyresponse2["results"][0]["n"]
                volume = polyresponse2["results"][0]["v"]
                with col1:

                    st.write(name + "'s Opening Price")
                    st.write(openprice)

                    st.write(name + "'s Closing Price")
                    st.write(closeprice)

                with col2:
                    st.write(name + "'s Lowest Price")
                    st.write(lowestprice)

                    st.write(name + "'s Highest Price")
                    st.write(highestprice)

                with col3:
                    st.write(name + "'s Number of Transcation")
                    st.write(ntrans)

                    st.write(name + "'s Trading Volume")
                    st.write(volume)

                st.success("Information Successfully Loaded from API")
            else:
                st.error("No ticker found, please check input")



    def map_creator(latitude,longitude):
        from streamlit_folium import folium_static
        import folium
        # center on the station
        m = folium.Map(location=[latitude, longitude], zoom_start=12)
        # add marker for the station
        folium.Marker([latitude, longitude], popup="HeadQuarters", tooltip="HeadQuarters").add_to(m)
        # call to render Folium map in Streamlit
        folium_static(m)

    #Streamlit SideBar Navigation
    st.sidebar.subheader("Stock Dashboard")

    #Input from the user in order to get a Stock
    userInput=  st.sidebar.text_input("Enter a valid stock ticker....GOOG")

    stock_ticker= userInput.upper()
    api_token= config.stockData_api_key

    if stock_ticker:
        parameters = {
        "symbols": stock_ticker,
        "api_token": api_token
        }
        stockData_url= "https://api.stockdata.org/v1/data/quote?"
        stockData= requests.get(stockData_url, params=parameters).json()


        st.title(stockData["data"][0]["name"] + "'s Dashboard")
        polystocks_url = "https://api.polygon.io/v3/reference/tickers/{}?apiKey=WJtsWZ032pndm6sfV4BAUnbaoOL7ku6X".format(
            stock_ticker)
        # Polygon.io Response from API
        polyresponse = requests.get(polystocks_url).json()
        col1, col2= st.columns(2)
        price()
        with col1:
            information()
        with col2:
            map()
    else:
        st.warning("Please input a Stock's ticker")

# testing
