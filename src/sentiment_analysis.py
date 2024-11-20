from bs4 import BeautifulSoup
from langchain_ollama.llms import OllamaLLM
from newspaper import Article
from textblob import TextBlob
import requests
import streamlit as st
import time


# Initialize Ollama LLM with the "smollm:135m" model
ollama_model = OllamaLLM(model="llama3.2:1b")

def fetch_news(symbol):
    search_url = f"https://www.google.com/search?q={symbol}+stock&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    news_elements = soup.select("div.SoaBEf")[:5]  # Fetch top 5 articles

    if news_elements:
        with st.spinner("Fetching and summarizing news articles..."):
            for idx, el in enumerate(news_elements):
                try:
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
                    summary_prompt = f"Summarize the following news article in 100 words. Focus on key details such as what happened, who is involved, why it is significant, and any notable outcomes or impacts. The summary should be short, clear, and informative without unnecessary details:\n\n{full_content}"
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

                    # Display the article in real-time
                    st.markdown(f"### [{title}]({link})")
                    st.write(f"**Published on:** {pub_date}")
                    st.write(f"**Source:** {source}")
                    st.write(f"**Headline Sentiment:** {headline_sentiment_label} ({headline_sentiment:.2f})")
                    st.write(f"**Content Sentiment:** {content_sentiment_label} ({content_sentiment:.2f})")

                    with st.expander("Summary of the Article"):
                        st.write(summary.strip())

                    # Additional metrics
                    st.write("**Metrics Analysis:**")
                    st.progress(abs(content_sentiment))  # Example progress bar based on sentiment score

                except Exception as e:
                    st.error(f"Failed to process an article: {e}")
                    continue

    return articles

def fetch_news(symbol):
    search_url = f"https://www.google.com/search?q={symbol}+stock&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    news_elements = soup.select("div.SoaBEf")[:5]  # Fetch top 5 articles

    if news_elements:
        with st.spinner("Fetching and summarizing news articles..."):
            for idx, el in enumerate(news_elements):
                try:
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
                    summary_prompt = f"Summarize the following article in about 50 words:\n\n{full_content}"
                    summary = ollama_model.predict(summary_prompt)

                    # Append article data
                    article_data = {
                        "headline": title,
                        "content": full_content,  # Full article text
                        "summary": summary.strip(),  # Summary of the article
                        "link": link,
                        "pub_date": pub_date,
                        "source": source
                    }
                    articles.append(article_data)

                    # Display the article in real-time
                    st.markdown(f"### [{title}]({link})")
                    st.write(f"**Published on:** {pub_date}")
                    st.write(f"**Source:** {source}")
                    with st.expander("Summary of the Article"):
                        st.write(summary.strip())

                except Exception as e:
                    st.error(f"Failed to process an article: {e}")
                    continue

                # Pause briefly to avoid overwhelming the server
                time.sleep(1)  # Add a delay to prevent rate limiting

    return articles
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
