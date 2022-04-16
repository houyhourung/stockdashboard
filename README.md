# The Stock Market

Our web application is built with streamlit with the goal of allowing the users to search for infomation about stock using stock ticker of a specific stock. 

## Team members:

Carolina Martinez, HouyHour Ung, Jairo Adarmes, Jose Ayala, , Alex Sabatier, Carlos Zamora

## Cloning the Repository:

>`git clone https://github.com/BackLeftGroup/stockmarket.git`

## Create the Virtual Environment for the Project:

### MacOS: 

>`python3 -m venv env && source ./env/bin/activate`

### Windows:

> `python3 -m venv env`\
> `env\Scripts\activate`

## Installing Streamlit:

>`pip install streamlit`

## Installing Dependent Packages:

>`pip install geopy`\
>`pip install streamlit-folium`

## API Key and Config File:

Getting API keys:
* **Polygon**: https://polygon.io/
* **StockData**: https://www.stockdata.org/
* **Alpha Vantage**: https://www.alphavantage.co/

Config file:
* Create an 'config.py' file
* Create three variable:
    > stockData_api_key = 'paste your api key'\
    > polygon_line_graph_api_key = 'paste your api key'\
    > alpha_vantage_api_key = 'paste your api key'
* Save the file 



## Running the App:

>`streamlit run app.py`



