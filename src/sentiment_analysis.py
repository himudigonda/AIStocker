import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

import requests
from bs4 import BeautifulSoup

def fetch_news(symbol):
    try:
        # Use Google News RSS for fetching stock news
        google_url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(google_url)
        soup = BeautifulSoup(response.content, "xml")
        headlines = []

        for item in soup.find_all("item")[:5]:
            title = item.title.text
            link = item.link.text
            pub_date = item.pubDate.text
            headlines.append((title, link, pub_date))  # Include title, link, and publication date

        return headlines
    except Exception as e:
        return []  # Return empty list if there's an error

from textblob import TextBlob

def analyze_sentiment(texts):
    """
    Analyze the sentiment of a list of texts using TextBlob.
    Returns a list of sentiment polarity scores.
    """
    if isinstance(texts, list):
        return [TextBlob(text).sentiment.polarity for text in texts]
    else:
        return TextBlob(texts).sentiment.polarity
