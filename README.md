Live app available <a href="https://edgar28oh-stockanalyzer-app-etloss.streamlit.app/" target="_blank">here</a>.

# Stock Analyzer Web App

The Stock Analyzer Web App is a simple Streamlit application that allows you to search for stock tickers, visualize their historical stock prices, and analyze the sentiment of recent news articles related to the selected stock ticker.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Introduction

The Stock Analyzer Web App is built using Python and the Streamlit framework. It leverages various libraries, such as yfinance for fetching historical stock data, BeautifulSoup for web scraping news articles, and NLTK's VADER SentimentIntensityAnalyzer for analyzing news sentiment. The app provides an interactive and user-friendly interface to perform stock analysis.

## Features

- **Stock Ticker Search**: Enter a stock ticker symbol to view the historical closing and opening prices for the selected stock.
- **Custom Date Range**: Choose a specific start and end date to analyze the stock's historical data.
- **Stock Metrics**: Display key metrics such as recommendation, forward PE, trailing PE, volume, market cap, short ratio, 50-day average, 52-week high, and 52-week low for the selected stock.
- **Raw Data Visualization**: View the raw data in a tabular format to explore the historical stock prices.
- **News Sentiment Analysis**: Analyze the sentiment of recent news articles related to the selected stock, visualized through a bar chart.

## Installation

1. Clone the repository to your local machine:

```git clone https://github.com/edgar28oh/stockAnalyzer.git```

```cd stockAnalyzer```


2. Install the required dependencies using pip:

```pip install -r requirements.txt```


## Usage

To run the Stock Analyzer Web App, execute the following command:

```streamlit run app.py```

The web app will open in your default web browser. Enter the stock ticker symbol and select the date range for analysis. Click on the "GO" button to view the stock's historical closing and opening prices, along with key metrics and news sentiment analysis.

## Dependencies

The Stock Analyzer Web App relies on the following libraries:

- datetime
- yfinance
- streamlit
- pandas
- matplotlib
- plotly
- BeautifulSoup
- nltk

All these dependencies are listed in the `requirements.txt` file and can be installed using `pip`.

## Contributing

Contributions to the Stock Analyzer Web App are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.



