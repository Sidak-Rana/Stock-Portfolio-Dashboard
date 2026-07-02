# Stock Portfolio Dashboard

An interactive stock portfolio tracker built with Python and Streamlit. It pulls live prices via `yfinance` and visualizes gains/losses, sector allocation, returns, and correlation between holdings.

**Live demo:** [portfolio-dashboard-app.streamlit.app](https://portfolio-dashboard-app.streamlit.app)

## Features

- **Table view** — live portfolio table with cost basis, market value, gains/losses, and percent return, plus top/bottom performer callouts
- **Returns view** — 1-year percent return chart for any individual ticker or all tickers overlaid
- **Distribution view** — portfolio allocation pie chart, sector allocation pie chart, a red-green gain/loss bar chart, and a correlation heatmap across holdings

## Tech stack

- Python
- Streamlit
- yfinance
- pandas
- Plotly

## How it works

- `App.py` — reads `portfolio.csv`, fetches current prices from yfinance (falling back through `currentPrice` → `regularMarketPrice` → `navPrice`), and computes derived columns (gains/losses, percent return, market value, cost basis)
- `dashboard.py` — the Streamlit UI, built on top of the data from `App.py`

## Running locally

1. Clone the repo:
   ```
   git clone https://github.com/Sidak-Rana/Stock-Portfolio-Dashboard.git
   cd Stock-Portfolio-Dashboard
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your holdings to `portfolio.csv` (columns: `Tickers`, `Shares`, `Average Costs`, `Sector`)
4. Run the app:
   ```
   streamlit run dashboard.py
   ```

## Notes

- `portfolio.csv` in this repo contains sample/placeholder holdings, not real portfolio data.
- Sector labels are assigned manually in the CSV, since yfinance's sector data is unreliable for ETFs.
