import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

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
        return []

def analyze_sentiment(texts):
    if isinstance(texts, list):
        return [TextBlob(text).sentiment.polarity for text in texts]
