import yfinance as yf
import requests

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


def interpret_company_metrics(company_info):
    """
    Analyze and interpret financial metrics for investment insights.
    """
    insights = []

    # Check and analyze P/E ratio
    if "P/E Ratio" in company_info and company_info["P/E Ratio"] != "N/A":
        pe_ratio = float(company_info["P/E Ratio"])
        if pe_ratio < 15:
            insights.append("The stock appears undervalued based on its P/E ratio.")
        elif pe_ratio > 25:
            insights.append("The stock might be overvalued compared to industry averages.")

    # Check and analyze Dividend Yield
    if "Dividend Yield" in company_info and company_info["Dividend Yield"] != "N/A":
        dividend_yield = float(company_info["Dividend Yield"].strip('%'))
        if dividend_yield > 2:
            insights.append("The company provides a competitive dividend yield, good for income-seeking investors.")

    # Check and analyze ROE and Debt-to-Equity
    if "ROE" in company_info and company_info["ROE"] != "N/A" and "Debt-to-Equity" in company_info:
        roe = float(company_info["ROE"].strip('%'))
        debt_to_equity = float(company_info["Debt-to-Equity"])
        if roe > 15 and debt_to_equity < 1:
            insights.append("The company is efficiently generating profits with manageable debt levels.")

    return insights

def get_company_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        company_name = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        forward_pe = info.get('forwardPE', 'N/A')
        eps = info.get('trailingEps', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        beta = info.get('beta', 'N/A')
        roe = info.get('returnOnEquity', 'N/A')
        profit_margin = info.get('profitMargins', 'N/A')
        revenue_growth = info.get('revenueGrowth', 'N/A')
        ebitda = info.get('ebitda', 'N/A')
        debt_to_equity = info.get('debtToEquity', 'N/A')
        fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')

        company_info = {
            "Company Name": company_name,
            "Sector": sector,
            "Industry": industry,
            "Market Cap": f"${market_cap:,}" if market_cap != 'N/A' else 'N/A',
            "P/E Ratio": pe_ratio,
            "Forward P/E Ratio": forward_pe,
            "EPS": eps,
            "Dividend Yield": f"{dividend_yield * 100:.2f}%" if dividend_yield != 'N/A' else 'N/A',
            "Beta": beta,
            "ROE (Return on Equity)": f"{roe * 100:.2f}%" if roe != 'N/A' else 'N/A',
            "Profit Margin": f"{profit_margin * 100:.2f}%" if profit_margin != 'N/A' else 'N/A',
            "Revenue Growth": f"{revenue_growth * 100:.2f}%" if revenue_growth != 'N/A' else 'N/A',
            "EBITDA": f"${ebitda:,}" if ebitda != 'N/A' else 'N/A',
            "Debt-to-Equity": debt_to_equity,
            "52-Week High": f"${fifty_two_week_high:.2f}" if fifty_two_week_high != 'N/A' else 'N/A',
            "52-Week Low": f"${fifty_two_week_low:.2f}" if fifty_two_week_low != 'N/A' else 'N/A',
        }

        return company_info

    except Exception as e:
        print(f"Error fetching company info: {e}")
        return {"Error": "Unable to retrieve company information."}
