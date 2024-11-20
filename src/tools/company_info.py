
import yfinance as yf
import requests
from bs4 import BeautifulSoup

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


def get_company_info(symbol):
    """
    Fetch detailed company information for the given stock symbol using Yahoo Finance.
    """
    try:
        stock = yf.Ticker(symbol)
        company_name = stock.info.get('longName', 'N/A')
        sector = stock.info.get('sector', 'N/A')
        industry = stock.info.get('industry', 'N/A')
        business_summary = stock.info.get('longBusinessSummary', 'N/A')[:500] + "..."

        return {
            "Company Name": company_name,
            "Sector": sector,
            "Industry": industry,
            "Business Summary": business_summary
        }
    except Exception as e:
        print(f"Error fetching company info: {e}")
        return None
