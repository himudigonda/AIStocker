import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news(symbol):
    try:
        # Use Yahoo Finance first
        url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        headlines = [headline.text for headline in soup.find_all('h3')[:5]]
        if headlines:
            return headlines

        # Fallback to Google News
        google_url = f"https://news.google.com/rss/search?q={symbol}+stock"
        news = requests.get(google_url).text
        soup = BeautifulSoup(news, "xml")
        headlines = [item.title.text for item in soup.find_all("item")[:5]]
        return headlines

    except Exception:
        return []

def analyze_sentiment(news_headlines):
    """
    Perform sentiment analysis on a list of news headlines.

    Args:
        news_headlines (list): List of headlines.

    Returns:
        List of sentiment scores.
    """
    sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
    return sentiment_scores
