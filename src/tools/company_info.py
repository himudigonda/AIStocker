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

def get_company_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return f"{info['longName']} ({symbol}) is a {info['industry']} company. {info['longBusinessSummary'][:200]}..."
