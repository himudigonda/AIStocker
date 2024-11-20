import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def analyze_sentiment(news_headlines):
    sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
    return sentiment_scores

def fetch_news(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [headline.text for headline in soup.find_all('h3')[:5]]
    return headlines
