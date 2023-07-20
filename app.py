import datetime
import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as gr_ob
from bs4 import BeautifulSoup
import nltk
nltk.download('vader_lexicon') # fix to deploy to streamlit
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.request import urlopen, Request


st.sidebar.subheader("""Stock Search Web App""")
selected_stock = st.sidebar.text_input("Enter Stock Ticker", "MSFT")
stock_ticker = yf.Ticker(selected_stock)

# ticker data parameters
today = datetime.date.today()
past = today - datetime.timedelta(days=365)
start_date = st.sidebar.date_input('Start date', past)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' %
                       (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

# go button
button_clicked = st.sidebar.button("GO")
if button_clicked == "GO":
    main()


# need to fix this caching issue
# @st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data

#url to pull the news articles
finviz = 'https://finviz.com/quote.ashx?t='
news_tables = {}
url = finviz + selected_stock
print(url)


def main():
    
    # load ticker hisroty, if ticker not found then user
    # enetered an incorrect ticker symbol
    try:
        data = load_data(selected_stock)
    # header
        st.header("""Daily **closing and openning price** for """ +
                stock_ticker.info['longName'])
    except:
        return st.warning("ENTER A CORRECT STOCK TICKER")

    st.subheader(
        ":red[WARNING: THIS IS NOT FINANCIAL ADVICE!]")

    # print line chart with daily closing prices for searched ticker
    def plot_raw_data():
        fig = gr_ob.Figure()
        fig.add_trace(gr_ob.Scatter(x=data['Date'],
                                    y=data['Open'], name='Stock Open'))
        fig.add_trace(gr_ob.Scatter(x=data['Date'],
                                    y=data['Close'], name='Stock Close'))
        fig.layout.update(
            xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    plot_raw_data()

    st.subheader("Metrics")
    # metric columns section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Recommendation",
                value=stock_ticker.info['recommendationKey'], delta="")
        st.metric(label="Foward PE",
                value=stock_ticker.info['forwardPE'], delta="")
        # some tickers don't generate a trailing PE
        # in order to avoid crashing I added a try block
        try:
            st.metric(label="Trailing PE",
                value=stock_ticker.info['trailingPE'], delta="")
        except:
            st.metric(label="Trailing PE",
                value=('No Data'), delta="")
    with col2:
        st.metric(label="Volume",
                value=stock_ticker.info['volume'], delta="")
        st.metric(label="Market Cap",
                value=stock_ticker.info['marketCap'], delta="")
        try:
            st.metric(label="Short Ratio",
                value=stock_ticker.info['shortRatio'], delta="")
        except:
            st.metric(label="Short Ratio",
                value=('No Data'), delta="")
        
    with col3:
        st.metric(label="50-day Average",
                value=stock_ticker.info['fiftyDayAverage'], delta="")
        st.metric(label="52-week High",
                value=stock_ticker.info['fiftyTwoWeekHigh'], delta="")
        st.metric(label="52-week Low",
                value=stock_ticker.info['fiftyTwoWeekLow'], delta="")

    st.subheader("Raw Data")
    st.write(data)

    # news sentiment section
    st.subheader("Recent News")
    finviz_url = 'https://finviz.com/quote.ashx?t='

    news_tables = {}
    # generate the url for the stock and then get the html of
    # the news table
    if selected_stock:
        url = finviz_url + selected_stock

        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)
        
        html = BeautifulSoup(response,'html')

        news_table = html.find(id='news-table')
        news_tables[selected_stock] = news_table
        
    parsed = []

    ticker_data = news_tables[selected_stock]
    ticker_rows = ticker_data.findAll('tr')

    for index, row in enumerate(ticker_rows):
        # this is a problem. some articles apparently dont have an 'a' tag which 
        # throws an error and prevents the parser from accessing the title
        if row.a:
            title = row.a.text
            link = row.a['href']
        else:
            pass

        ts = row.td.text.strip()

        if len(ts) < 10:
            time = ts
        else:
            date = ts[:9]
            time = ts[10:]
        parsed.append([date + " " + time, title, link])

    
    df = pd.DataFrame(parsed, columns=['date', 'title', 'link'])
    
    st.dataframe(df.head(10))

    vader = SentimentIntensityAnalyzer()
    df['compound'] = df['title'].apply(lambda title: vader.polarity_scores(title)['compound'])
    
    df['date'] = pd.to_datetime(df.date).dt.date

    mean_data = df.groupby(['date']).mean(numeric_only=True)
    mean_data = mean_data.unstack()
    mean_data = mean_data.xs('compound').transpose()

    st.subheader("News Sentiment Analysis")
    st.bar_chart(mean_data)
    stock_ticker.info


if __name__ == "__main__":
    main()



