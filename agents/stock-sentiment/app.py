import streamlit as st
import yfinance as yf
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Stock Sentiment Analyst", page_icon="📈")

st.title("📉 Stock Market Sentiment Analyst")
st.markdown("Analyze latest news and market data to determine bull/bear sentiment for any ticker.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    period = st.selectbox("Historical Context", ["1d", "5d", "1mo"])

ticker = st.text_input("Enter Ticker Symbol (e.g. AAPL, TSLA, NVDA):", value="AAPL").upper()

if st.button("Analyze Sentiment 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        try:
            with st.spinner(f"Fetching data for {ticker}..."):
                stock = yf.Ticker(ticker)
                news = stock.news[:5] # Get 5 latest news items
                
                if not news:
                    st.warning("No recent news found for this ticker.")
                else:
                    llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
                    
                    news_titles = "\n".join([item['title'] for item in news])
                    
                    prompt = PromptTemplate(
                        input_variables=["ticker", "news"],
                        template="""
                        You are a Financial Analyst. Based on the following news headlines for {ticker}, 
                        analyze the overall sentiment. 

                        Headlines:
                        {news}

                        Provide:
                        - Sentiment Score (1-10, where 10 is very Bullish)
                        - Core Sentiment (Bullish/Bearish/Neutral)
                        - 3 Key Market Drivers from these headlines.
                        """
                    )
                    
                    response = llm.predict(prompt.format(ticker=ticker, news=news_titles))
                    
                    st.success("Analysis Complete!")
                    st.markdown(f"### Results for {ticker}")
                    st.markdown(response)
                    
                    # Also show ticker basic info
                    st.markdown("---")
                    st.write(f"**Current Price:** ${stock.fast_info['lastPrice']:.2f}")
                    st.write(f"**Day Change:** {stock.fast_info['dayChange']:.2f}%")
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) hub.")
