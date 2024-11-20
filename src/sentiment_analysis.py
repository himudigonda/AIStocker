import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import time

def fetch_news(symbol):
    """
    Fetches the latest articles for a given stock symbol and extracts their content from the actual source.
    """
    try:
        google_url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(google_url)
        soup = BeautifulSoup(response.content, "xml")

        articles = []

        for item in soup.find_all("item")[:5]:  # Fetch top 5 articles
            headline = item.title.text
            redirect_link = item.link.text
            pub_date = item.pubDate.text

            # Resolve the Google News redirect link
            try:
                resolved_response = requests.get(redirect_link, allow_redirects=True)
                actual_link = resolved_response.url

                # Fetch article content
                article_response = requests.get(actual_link, headers={"User-Agent": "Mozilla/5.0"})
                article_soup = BeautifulSoup(article_response.content, "html.parser")

                # Extract paragraphs or fallback to plain text
                paragraphs = article_soup.find_all('p')
                content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

                if not content.strip():
                    content = article_soup.get_text(separator="\n").strip()

                articles.append({
                    "headline": headline,
                    "content": content,  # Store full content here
                    "link": actual_link,
                    "pub_date": pub_date
                })
                time.sleep(1)

            except Exception as e:
                print(f"Failed to fetch content from {redirect_link}: {e}")
                continue

        return articles

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
        print(f"Error fetching news: {e}")
        return []



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
