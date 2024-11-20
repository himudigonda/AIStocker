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


def get_company_info(symbol):
    """
    Fetch detailed company information including financial metrics, annual reports, and more.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        company_name = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        business_summary = info.get('longBusinessSummary', 'N/A')[:500] + "..."
        market_cap = info.get('marketCap', 'N/A')
        revenue = info.get('totalRevenue', 'N/A')
        net_income = info.get('netIncomeToCommon', 'N/A')
        eps = info.get('trailingEps', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        roe = info.get('returnOnEquity', 'N/A')
        roa = info.get('returnOnAssets', 'N/A')
        debt_to_equity = info.get('debtToEquity', 'N/A')

        # Fetch the link to the latest annual report
        annual_report_url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={symbol}&action=getcompany&type=10-k"

        return {
            "Company Name": company_name,
            "Sector": sector,
            "Industry": industry,
            "Business Summary": business_summary,
            "Market Cap": f"${market_cap:,}" if market_cap != 'N/A' else 'N/A',
            "Revenue": f"${revenue:,}" if revenue != 'N/A' else 'N/A',
            "Net Income": f"${net_income:,}" if net_income != 'N/A' else 'N/A',
            "EPS": eps,
            "P/E Ratio": pe_ratio,
            "Dividend Yield": f"{dividend_yield * 100:.2f}%" if dividend_yield != 'N/A' else 'N/A',
            "ROE": f"{roe * 100:.2f}%" if roe != 'N/A' else 'N/A',
            "ROA": f"{roa * 100:.2f}%" if roa != 'N/A' else 'N/A',
            "Debt-to-Equity": debt_to_equity,
            "Annual Report": annual_report_url
        }
    except Exception as e:
        print(f"Error fetching company info: {e}")
        return None
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
