import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news(symbol):
    """
    Fetch the latest news articles related to the stock symbol from Google News.
    """
    try:
        url = f"https://news.google.com/rss/search?q={symbol}+stock"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "xml")

        news_items = []
        for item in soup.find_all("item")[:5]:
            title = item.title.text
            link = item.link.text
            pub_date = item.pubDate.text
            sentiment = analyze_sentiment(title)
            news_items.append({"headline": title, "link": link, "date": pub_date, "sentiment": sentiment})

        return news_items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text using TextBlob.
    Returns a sentiment polarity score.
    """
    return TextBlob(text).sentiment.polarity
