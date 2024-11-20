import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news(symbol):
    try:
        google_url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(google_url)
        soup = BeautifulSoup(response.content, "xml")
        headlines = [(item.title.text, item.link.text, item.pubDate.text) for item in soup.find_all("item")[:5]]
        return headlines
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(texts):
    """
    Returns sentiment polarity scores for each text in the list.
    Positive (> 0), Neutral (0), Negative (< 0).
    """
    if isinstance(texts, list):
        return [TextBlob(text).sentiment.polarity for text in texts]
    else:
        return []
