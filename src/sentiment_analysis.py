import requests
from bs4 import BeautifulSoup

def analyze_sentiment(news_headlines):
    """
    Perform sentiment analysis on a list of news headlines.

    Args:
        news_headlines (list): List of headlines.

    Returns:
        List of sentiment scores.
    """
    from textblob import TextBlob
    sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
    return sentiment_scores

def fetch_news(symbol):
    """
    Fetch recent news articles related to a stock symbol.

    Args:
        symbol (str): Stock ticker symbol.

    Returns:
        list: List of headlines.
    """
    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = [headline.text for headline in soup.find_all('h3')[:5]]
    return headlines
