import streamlit as st
import plotly.express as px
import yfinance as yf
import pandas as pd
import datetime
from App import df, get_price, calc_gain_loss, percent_return

st.set_page_config(layout="wide")

def get_history(symbol):
    if "." in symbol:
        symbol = symbol.replace(".", "-")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1y')
    if hist.empty:
        return None
    close = hist['Close']
    return ((close / close.iloc[0]) - 1) * 100

def get_price_history(symbol):
    if "." in symbol:
        symbol = symbol.replace(".", "-")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1y')
    if hist.empty:
        return None
    return hist['Close']

##skeleton of streamlit webpage
st.title("Finance Portfolio Dashboard")
view = st.sidebar.radio("View", ["Table", "Returns", "Distribution"])

if view == "Table":
    col1, col2, col3, col4, col5, _ = st.columns([1, 1, 1, 1, 1, 3])
    with col1:
        st.metric(label = "Cost Basis", value=f"${df['Cost Basis'].sum():.2f}")
    with col2:
        st.metric(label = "Total Value", value=f"${df['Market Values'].sum():.2f}", delta=f"${df['Gains and Losses'].sum():.2f}")
    with col3:
        st.metric(label = "Overall Percent Return", value=f"{(df["Gains and Losses"].sum() / df["Cost Basis"].sum()) * 100:.2f}%")
    with col4:
        top = df.loc[df["Percent Returns"].idxmax()]
        st.metric(label="Top Performer", value=top["Tickers"], delta=f"{top['Percent Returns']:.2f}%")
    with col5:
        bot = df.loc[df["Percent Returns"].idxmin()]
        st.metric(label="Worst Performer", value=bot["Tickers"], delta=f"{bot['Percent Returns']:.2f}%")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df, hide_index = True)
        st.caption(f"Last Updated: {datetime.datetime.now()}")

elif view == "Returns":
    tickers = ["All"] + list(df["Tickers"])
    selected = st.selectbox("select Ticker", tickers)
    hist_dict = {}
    if selected == "All":
        with st.spinner("Fetching history..."):
            for symbol in df["Tickers"]:
                result = get_history(symbol)
                if result is not None:
                    hist_dict[symbol] = result
        hist_df = pd.DataFrame(hist_dict)
        fig = px.line(hist_df, title = "All Tickers % Return (1Y)", labels = {"value": "% Return", "variable": "Ticker"})
        st.plotly_chart(fig)
    else:
        with st.spinner("Fetching history..."):
            hist = get_history(selected)
        fig = px.line(hist, title = f"{selected} % Return (1Y)", labels = {"value": "% Return", "variable": "Ticker"})
        st.plotly_chart(fig)
    st.caption(f"Last Updated: {datetime.datetime.now()}")

elif view == "Distribution":
    price_dict = {}
    ##plotly pie chart for portfolio distribution
    portfolio_dis = px.pie(df, names = "Tickers", values = "Market Values", title = "Portfolio Distribution")
    gain_loss_bar = px.bar(df, x = "Tickers", y = "Gains and Losses", color = "Gains and Losses", color_continuous_scale = "RdYlGn", color_continuous_midpoint = 0, title = "Gains and Losses")
    port_sector_dis = px.pie(df.groupby("Sector")["Market Values"].sum().reset_index(), names = "Sector", values = "Market Values", title = "Portfolio Sector Distribution")
    
    for symbol in df["Tickers"]:
        result = get_price_history(symbol)
        if result is not None:
            price_dict[symbol] = result
    price_df = pd.DataFrame(price_dict)
    corr = price_df.corr()
    corr_fig = px.imshow(corr, color_continuous_scale = "RdYlGn", title = "Correlation Heatmap")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(portfolio_dis, use_container_width=True)
        st.plotly_chart(port_sector_dis, use_container_width=True)
    with col2:
        st.plotly_chart(gain_loss_bar, use_container_width=True)
        st.plotly_chart(corr_fig, use_container_width = True)
    st.caption(f"Last Updated: {datetime.datetime.now()}")



