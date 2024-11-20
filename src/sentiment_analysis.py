from newspaper import Article
import requests
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news(symbol):
    search_url = f"https://www.google.com/search?q={symbol}+stock&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for el in soup.select("div.SoaBEf")[:5]:  # Fetch top 5 articles
        try:
            link = el.find("a")["href"]
            title = el.select_one("div.MBeuO").get_text()
            pub_date = el.select_one(".LfVVr").get_text()
            source = el.select_one(".NUnG9d span").get_text()

            article = Article(link)
            article.download()
            article.parse()

            content = article.text
            print(f"?title: {title}")
            print(f"?content: {content}")

            articles.append({
                "headline": title,
                "content": content[:10000],  # Limit content for preview
                "link": link,
                "pub_date": pub_date,
                "source": source
            })
            time.sleep(1)  # Avoid rate limiting

        except Exception as e:
            print(f"Failed to fetch content from {link}: {e}")
            continue

    return articles


def analyze_sentiment(articles):
    """
    Analyze sentiment for both the headline and the content of each article.
    """
    analyzed_articles = []

    for article in articles:
        try:
            headline_sentiment_score = TextBlob(article['headline']).sentiment.polarity
            content_sentiment_score = TextBlob(article['content']).sentiment.polarity

            # Classify sentiment as Positive, Neutral, or Negative
            def classify_sentiment(score):
                if score > 0.1:
                    return "Positive"
                elif score < -0.1:
                    return "Negative"
                else:
                    return "Neutral"

            analyzed_articles.append({
                "headline": article["headline"],
                "headline_sentiment": classify_sentiment(headline_sentiment_score),
                "content_sentiment": classify_sentiment(content_sentiment_score),
                "content": article["content"][:500],  # Show a preview of the content (first 500 chars)
                "link": article["link"],
                "pub_date": article["pub_date"]
            })

        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            continue

    return analyzed_articles
