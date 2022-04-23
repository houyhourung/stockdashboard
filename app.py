from ast import AsyncFunctionDef
from pyparsing import line
import numpy as np
import streamlit as st  # Streamlit Application
import requests
import pandas as pd
import csv

# Changes the Favicon and Tab Title
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

page = st.sidebar.selectbox("Choose your page", ["Home", "Stock Search"])

if page == "Home":
    # Display details of page 1
    # method to display interactive table
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


    # Bar graph created to compare popular stock prices
    def bar_graph():
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
            'Stock Price (USD)': [2567.49, 167.66, 282.06, 130.84, 3015.75, 79.79, 48.83, 153.23, 31.99, 33.45, 108.25,
                                  231.34, 44.48, 47.35],
        }).set_index('index')
        # displaying bar-chart
        st.bar_chart(data)
        # Two widgets created for bar customization (width and height)



    # Adding a page for the line chart
    def prueba():
        popular_stocks = pd.read_csv('Popular_Stocks2.csv')

        # Widget (if check box is selected displays Chart data size)
        amountElements = st.sidebar.checkbox(
            'Show Quantity of Stocks Graphed')

        # Widget (on the side bar showing which line graph you would like to see)
        element = st.sidebar.radio(
            "Select elements displayed in Line Chart",
            ('Price', 'high', 'low', 'all'))
        if element == 'Price':
            d = {'Price': popular_stocks["Price"]}
            chart_data = pd.DataFrame(
                data=d)

            st.line_chart(chart_data)
            if amountElements:
                st.write("Quantity:", chart_data.size)
        elif element == 'low':
            d = {'low': popular_stocks["Low"]}
            chart_data = pd.DataFrame(
                data=d)

            st.line_chart(chart_data)
            if amountElements:
                st.write("Quantity:", chart_data.size)
        elif element == 'high':
            d = {'high': popular_stocks["High"]}
            chart_data = pd.DataFrame(
                data=d)

            st.line_chart(chart_data)
            if amountElements:
                st.write("Quantity:", chart_data.size)
        elif element == 'all':
            d = {'Price': popular_stocks["Price"], 'high': popular_stocks["High"], 'low': popular_stocks["Low"]}
            chart_data = pd.DataFrame(
                data=d)

            st.line_chart(chart_data)
            if amountElements:
                st.write("Quantity:", chart_data.size)


    pass

    interactive_table()
    st.subheader("Popular Stocks in the Market (Price Comparison)")
    # Warning, requested by professor, to document static data.
    st.warning("Stock prices are not updated in real time.")
    col1, col2 = st.columns(2)
    with col1:
        prueba()
    with col2:
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
                    address1 = polyresponse["results"]["address"]["address1"], polyresponse["results"]["address"][
                        "city"], \
                               polyresponse["results"]["address"]["state"]
                    st.subheader(stockData["data"][0]["name"] + "'s Headquarter")
                    # Import geopy and geolocator
                    from geopy.geocoders import Nominatim

                    geolocator = Nominatim(user_agent="stock dashboard")

                    # Getting logitude and latitude from address
                    data = geolocator.geocode(address1)

                    # Checking to see if either longitude or latidue is empty
                    if data == None:
                        st.error("There is no address avaliable")
                    else:
                        latitude = data.latitude
                        longitude = data.longitude
                        map_creator(latitude, longitude)
                else:
                    st.error("There is no address avaliable")

            else:
                st.error("Please check the Ticker Symbol you have submitted and try again")

        pass


    def price():
        name = stockData["data"][0]["name"]
        st.subheader(name + "'s Previous Day Closing Information")
        col1, col2, col3 = st.columns(3)
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

    # Creating line graph
    def linegraph():
        alpha_vantage_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(
            stock_ticker, st.secrets["alpha_vantage_api_key"])
        line_stock_data = requests.get(alpha_vantage_url).json()
        # creating graph using DataFrame
        data = pd.DataFrame.from_dict(line_stock_data['Time Series (Daily)'], orient='index').sort_index(axis=1)
        data = data.rename(
            columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        # showing the last 5 days open, high, low, close, and volume price of the stock
        st.line_chart(data=data.head(5))


    def calculator():
        st.subheader("Stock Equity Calculator")
        col1, col2 = st.columns(2)
        with col1:
            name = stockData["data"][0]["name"]
            number = st.number_input('Insert the amount of Stock you would like to buy of ' + name)
            highestprice = (polyresponse2["results"][0]["h"])
            totalhighest = (highestprice * number)
            lowestprice = (polyresponse2["results"][0]["l"])
            totallowest = (lowestprice * number)
            openprice = (polyresponse2["results"][0]["o"])
            totalopen = (openprice * number)
        with col2:
            st.write("Had you bought today at:")
            st.write("Highest Price, you would have needed to have an equity of about: ")
            st.write(totalhighest)
            st.write("Lowest Price, you would have needed to have an equity of about: ")
            st.write(totallowest)
            st.write("Open Price, you would have needed to have an equity of about: ")
            st.write(totalopen)
            st.warning("This is only done to give user's an estimate to how much equity one would need. "
                       "Does not include taxes and other fees")


    def map_creator(latitude, longitude):
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

    # Input from the user in order to get a Stock
    userInput = st.sidebar.text_input("Enter a valid stock ticker....GOOG")

    stock_ticker = userInput.upper()
    api_token = st.secrets["stockData_api_key"]

    if stock_ticker:
        parameters = {
            "symbols": stock_ticker,
            "api_token": api_token
        }

        stockData_url = "https://api.stockdata.org/v1/data/quote?"
        stockData = requests.get(stockData_url, params=parameters).json()

        if not stockData["data"]:
            st.error("Please check your stock ticker input and try again")
        else:
            st.title(stockData["data"][0]["name"] + "'s Dashboard")
            polystocks_url = "https://api.polygon.io/v3/reference/tickers/{}?apiKey={}".format(
                stock_ticker, st.secrets["polygon_line_graph_api_key"])
            # Polygon.io Response from API
            polyresponse = requests.get(polystocks_url).json()
            polystocks_url2 = "https://api.polygon.io/v2/aggs/ticker/{}/" \
                              "prev?adjusted=true&apiKey={}".format(stock_ticker, st.secrets["polygon_line_graph_api_key"])
            polyresponse2 = requests.get(polystocks_url2).json()

            col1, col2 = st.columns(2)     
            with col1:
                information()
            with col2:
                map()
            price()
            calculator()
            st.subheader(stockData["data"][0]["name"] + "'s Last 5 Days Prices (open, high, low, close) and Volumes")
            linegraph()

    else:
        st.warning("Please input a Stock's ticker")


# testing

