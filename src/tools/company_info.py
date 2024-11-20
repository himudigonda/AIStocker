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

    # Analyze P/E ratio
    if company_info['P/E Ratio'] != 'N/A':
        if float(company_info['P/E Ratio']) < 15:
            insights.append("The stock appears undervalued based on its P/E ratio.")
        elif float(company_info['P/E Ratio']) > 25:
            insights.append("The stock might be overvalued compared to industry averages.")

    # Analyze Dividend Yield
    if company_info['Dividend Yield'] != 'N/A' and float(company_info['Dividend Yield'].strip('%')) > 2:
        insights.append("The company provides a competitive dividend yield, good for income-seeking investors.")

    # Analyze ROE and Debt-to-Equity
    if company_info['ROE'] != 'N/A' and company_info['Debt-to-Equity'] != 'N/A':
        roe = float(company_info['ROE'].strip('%'))
        debt_to_equity = float(company_info['Debt-to-Equity'])

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
        business_summary = info.get('longBusinessSummary', 'N/A')[:500] + "..."
        quarterly_growth = info.get('revenueQuarterlyGrowth', 'N/A')
        peg_ratio = info.get('pegRatio', 'N/A')
        earnings_date = info.get('nextEarningsDate', 'N/A')

        return {
            "Company Name": company_name,
            "Sector": sector,
            "Industry": industry,
            "Business Summary": business_summary,
            "Quarterly Growth": quarterly_growth,
            "PEG Ratio": peg_ratio,
            "Next Earnings Date": earnings_date
        }
    except Exception as e:
        print(f"Error fetching company info: {e}")
        return {"Error": "Unable to retrieve company information."}
