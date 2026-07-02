import numpy as np
import pandas as pd 
import yfinance as yf


df = pd.read_csv("portfolio.csv")
df = df.sort_values(by='Shares', ascending=False)

def get_price(symbol): #gets the price of a ticker 
    if "." in symbol:
        symbol = symbol.replace(".", "-")
    ticker = yf.Ticker(symbol)
    tdys_data = ticker.info.get("currentPrice")
    if tdys_data is None:
        tdys_data = ticker.info.get("regularMarketPrice")
    if tdys_data is None:
        tdys_data = ticker.info.get("navPrice")
    return tdys_data

def calc_gain_loss(shares, avg_cost, cur_price):
    gain_loss = (cur_price-avg_cost)*shares
    return gain_loss

def percent_return(avg_cost, cur_price):
    preturn = ((cur_price-avg_cost)/avg_cost)*100
    return preturn

def compute_columns():
    current_costs = []
    gains_losses = []
    percent_returns = []
    market_values = []
    cost_basis = []
    for index, row in df.iterrows():
        symbol = row["Tickers"]
        shares = row["Shares"]
        avg_cost = row["Average Costs"]
        cur_cost = get_price(symbol)
        gain_loss = round(calc_gain_loss(shares, avg_cost, cur_cost), 4)
        preturn = round(percent_return(avg_cost, cur_cost), 4)
        mar_cost = shares*cur_cost
        cost_base = shares * avg_cost
        current_costs.append(cur_cost), gains_losses.append(gain_loss), percent_returns.append(preturn), market_values.append(mar_cost), cost_basis.append(cost_base)
    df['Current Costs'] = current_costs
    df['Gains and Losses'] = gains_losses
    df['Percent Returns'] = percent_returns
    df['Market Values'] = market_values
    df['Cost Basis'] = cost_basis

compute_columns()

def main():
    print(f"{"Tickers":<10}{"Shares":<10}{"Average Costs":<15}{"Current Costs":<15}{"Gains and Losses":<18}{"Percent Returns":<22}\n")
    for index, row in df.iterrows():
        print(f"{row['Tickers']:<10}{row['Shares']:<10}{row['Average Costs']:<15}{row['Current Costs']:<15}{row['Gains and Losses']:<18}{row['Percent Returns']:<22}")
    print(df)


if __name__ == "__main__":
    main()