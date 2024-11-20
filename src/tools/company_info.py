
import requests
from bs4 import BeautifulSoup
import yfinance as yf

get_company_info_schema = {
    "name": "get_company_info",
    "description": "Get basic information about a company",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol, e.g. AAPL for Apple",
            },
        },
        "required": ["symbol"],
    },
}

import requests
import yfinance as yf

def get_company_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        company_name = stock.info.get('longName', None)
        industry = stock.info.get('industry', None)
        sector = stock.info.get('sector', None)
        business_summary = stock.info.get('longBusinessSummary', None)

        if not company_name or not business_summary:
            raise ValueError("Incomplete data from Yahoo Finance.")

        company_info = {
            "Company Name": company_name,
            "Industry": industry,
            "Sector": sector,
            "Business Summary": business_summary[:300] + "..." if business_summary else "N/A"
        }
        return company_info
    except Exception:
        return fetch_from_backup(symbol)

def fetch_from_backup(symbol):
    try:
        # Use a backup API to fetch company data
        url = f"https://api.polygon.io/v3/reference/tickers/{symbol}?apiKey=YOUR_POLYGON_API_KEY"
        response = requests.get(url).json()
        result = response['results']

        return {
            "Company Name": result['name'],
            "Industry": result.get('sic_description', 'N/A'),
            "Sector": result.get('sector', 'N/A'),
            "Business Summary": result.get('description', 'Summary Not Available')
        }
    except:
        return {"Error": "Unable to retrieve company information. Multiple sources failed."}
