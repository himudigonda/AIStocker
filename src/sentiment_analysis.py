from bs4 import BeautifulSoup
from langchain_ollama.llms import OllamaLLM
from newspaper import Article
from textblob import TextBlob
import requests
import streamlit as st
import time

# Initialize Ollama LLM with the "smollm:135m" model
ollama_model = OllamaLLM(model="llama3.2:1b")


class NewsCache:
    def __init__(self):
        self.cache = {}

    def get(self, symbol):
        # Check if the symbol exists in the cache
        if symbol in self.cache:
            # Check if the cached data is less than 15 minutes old
            if time.time() - self.cache[symbol]["timestamp"] < 900:  # 900 seconds = 15 minutes
                return self.cache[symbol]["data"]
        return None

    def set(self, symbol, data):
        self.cache[symbol] = {
            "data": data,
            "timestamp": time.time()
        }

news_cache = NewsCache()

def fetch_news(symbol):
    # Check the cache
    cached_data = news_cache.get(symbol)
    if cached_data is not None:
        print(f"Using cached news for {symbol}.")
        return cached_data

    # Fetch news as usual if not cached
    search_url = f"https://www.google.com/search?q={symbol}+stock&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    news_elements = soup.select("div.SoaBEf")[:10]  # Fetch up to 10 articles to account for replacements
    max_articles = 5  # Target number of valid articles
    valid_articles_count = 0

    if news_elements:
        progress = st.progress(0)  # Initialize progress bar
        total_elements = len(news_elements)

        with st.spinner("Fetching and summarizing news articles..."):
            for idx, el in enumerate(news_elements):
                try:
                    if valid_articles_count >= max_articles:
                        break  # Stop when we have the required number of valid articles

                    link = el.find("a")["href"]
                    title = el.select_one("div.MBeuO").get_text()
                    pub_date = el.select_one(".LfVVr").get_text()
                    source = el.select_one(".NUnG9d span").get_text()

                    # Download article content
                    article = Article(link)
                    article.download()
                    article.parse()

                    # Full content of the article
                    full_content = article.text

                    # Summarize the article
                    summary_prompt = f"Summarize the following news article in 100 words. Focus on key details such as what happened, who is involved, why it is significant, and any notable outcomes or impacts. The summary should be short, clear, and informative:\n\n{full_content}"
                    summary = ollama_model.predict(summary_prompt)

                    # Perform sentiment analysis
                    headline_sentiment = TextBlob(title).sentiment.polarity
                    content_sentiment = TextBlob(full_content).sentiment.polarity

                    def classify_sentiment(score):
                        if score > 0.1:
                            return "Positive"
                        elif score < -0.1:
                            return "Negative"
                        else:
                            return "Neutral"

                    headline_sentiment_label = classify_sentiment(headline_sentiment)
                    content_sentiment_label = classify_sentiment(content_sentiment)

                    # Append article data
                    article_data = {
                        "headline": title,
                        "content": full_content,
                        "summary": summary.strip(),
                        "link": link,
                        "pub_date": pub_date,
                        "source": source,
                        "headline_sentiment": headline_sentiment_label,
                        "content_sentiment": content_sentiment_label,
                        "headline_sentiment_score": headline_sentiment,
                        "content_sentiment_score": content_sentiment,
                    }
                    articles.append(article_data)
                    valid_articles_count += 1

                except Exception as e:
                    print(f"Failed to process an article: {e}")
                    continue

                # Update progress bar
                progress.progress((idx + 1) / total_elements)

        progress.progress(1.0)  # Ensure progress bar is fully completed

    # Save the results in the cache
    news_cache.set(symbol, articles)

    return articles


def display_articles(articles):
    """
    Display all articles with sentiment and summary after processing.
    """
    for article in articles:
        st.markdown(f"### [{article['headline']}]({article['link']})")
        st.write(f"**Published on:** {article['pub_date']}")
        st.write(f"**Source:** {article['source']}")
        st.write(f"**Headline Sentiment:** {article['headline_sentiment']} ({article['headline_sentiment_score']:.2f})")
        st.write(f"**Content Sentiment:** {article['content_sentiment']} ({article['content_sentiment_score']:.2f})")

        with st.expander("Summary of the Article"):
            st.write(article["summary"])

        st.write("**Metrics Analysis:**")
        st.progress(abs(article["content_sentiment_score"]))  # Example progress bar based on sentiment score




def analyze_sentiment(articles):
    """
    Analyze sentiment for both the headline and the summarized content of each article.
    """
    analyzed_articles = []

    for article in articles:
        try:
            # Analyze sentiment
            headline_sentiment_score = TextBlob(article["headline"]).sentiment.polarity
            summary_sentiment_score = TextBlob(article["summary"]).sentiment.polarity

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
                "content_sentiment": classify_sentiment(summary_sentiment_score),
                "summary": article["summary"],  # Use the 50-word summary
                "link": article["link"],
                "pub_date": article["pub_date"]
            })

        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            continue

    return analyzed_articles
