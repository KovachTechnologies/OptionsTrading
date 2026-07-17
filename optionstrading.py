import os
from datetime import datetime, timedelta
from polygon import RESTClient
import pandas as pd

# ========================= CONFIG =========================
API_KEY = "YOUR_POLYGON_API_KEY_HERE"   # Get free at polygon.io
WATCHLIST = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN", "META", "AMD", "SPY", "QQQ"]  # Add more
DTE_TARGET_MIN = 25
DTE_TARGET_MAX = 40
MIN_CREDIT_PCT_OF_WIDTH = 0.25   # e.g., 25% of spread width
WIDTH_POINTS = 5                 # or 10 for wider spreads
MIN_OPEN_INTEREST = 50
# =========================================================

client = RESTClient(API_KEY)

def days_to_expiration(exp_date_str):
    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
    return (exp_date - datetime.now().date()).days

def get_best_credit_spreads(ticker):
    try:
        chain = list(client.list_snapshot_options_chain(ticker))
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return []

    opportunities = []
    today = datetime.now().date()

    # Filter to ~30 DTE options
    relevant = []
    for item in chain:
        details = item.details
        dte = days_to_expiration(details.expiration_date)
        if DTE_TARGET_MIN <= dte <= DTE_TARGET_MAX and item.open_interest >= MIN_OPEN_INTEREST:
            relevant.append((dte, item))

    if not relevant:
        return []

    # Group by expiry (use the closest to target)
    expiries = sorted(set(item[1].details.expiration_date for item in relevant))
    target_exp = expiries[0]  # simplest: first available in range

    puts = [item for dte, item in relevant if item.details.contract_type == "put" and item.details.expiration_date == target_exp]
    calls = [item for dte, item in relevant if item.details.contract_type == "call" and item.details.expiration_date == target_exp]

    # Sort by strike
    puts.sort(key=lambda x: x.details.strike_price)
    calls.sort(key=lambda x: x.details.strike_price)

    # === BULL PUT CREDIT SPREADS ===
    for i in range(len(puts) - 1):
        long_put = puts[i]      # lower strike
        short_put = puts[i + 1] # higher strike
        if short_put.details.strike_price - long_put.details.strike_price != WIDTH_POINTS:
            continue

        # Use mid prices
        short_mid = (short_put.last_quote.bid + short_put.last_quote.ask) / 2
        long_mid = (long_put.last_quote.bid + long_put.last_quote.ask) / 2
        credit = short_mid - long_mid
        if credit <= 0 or credit / WIDTH_POINTS < MIN_CREDIT_PCT_OF_WIDTH:
            continue

        delta_short = getattr(short_put.greeks, 'delta', 0)
        max_loss = WIDTH_POINTS - credit
        roc = (credit / max_loss) * 100 if max_loss > 0 else 0
        breakeven = short_put.details.strike_price - credit

        opportunities.append({
            "Ticker": ticker,
            "Type": "Bull Put Credit",
            "Expiry": target_exp,
            "DTE": days_to_expiration(target_exp),
            "Short Strike": short_put.details.strike_price,
            "Long Strike": long_put.details.strike_price,
            "Credit": round(credit, 2),
            "Max Loss": round(max_loss, 2),
            "ROC %": round(roc, 1),
            "Short Delta": round(delta_short, 3),
            "Breakeven": round(breakeven, 2),
            "IV": round(short_put.implied_volatility * 100, 1)
        })

    # === BEAR CALL CREDIT SPREADS (optional mirror) ===
    for i in range(len(calls) - 1):
        short_call = calls[i]     # lower strike
        long_call = calls[i + 1]  # higher strike
        if long_call.details.strike_price - short_call.details.strike_price != WIDTH_POINTS:
            continue

        short_mid = (short_call.last_quote.bid + short_call.last_quote.ask) / 2
        long_mid = (long_call.last_quote.bid + long_call.last_quote.ask) / 2
        credit = short_mid - long_mid
        if credit <= 0 or credit / WIDTH_POINTS < MIN_CREDIT_PCT_OF_WIDTH:
            continue

        delta_short = getattr(short_call.greeks, 'delta', 0)
        max_loss = WIDTH_POINTS - credit
        roc = (credit / max_loss) * 100 if max_loss > 0 else 0
        breakeven = short_call.details.strike_price + credit

        opportunities.append({
            "Ticker": ticker,
            "Type": "Bear Call Credit",
            "Expiry": target_exp,
            "DTE": days_to_expiration(target_exp),
            "Short Strike": short_call.details.strike_price,
            "Long Strike": long_call.details.strike_price,
            "Credit": round(credit, 2),
            "Max Loss": round(max_loss, 2),
            "ROC %": round(roc, 1),
            "Short Delta": round(delta_short, 3),
            "Breakeven": round(breakeven, 2),
            "IV": round(short_call.implied_volatility * 100, 1)
        })

    return opportunities

# ========================= RUN SCANNER =========================
all_opps = []
print("Scanning for credit spread opportunities...\n")
for ticker in WATCHLIST:
    opps = get_best_credit_spreads(ticker)
    all_opps.extend(opps)

if all_opps:
    df = pd.DataFrame(all_opps)
    # Sort by best risk/reward
    df = df.sort_values(by=["ROC %", "Credit"], ascending=False)
    print(df.to_string(index=False))
    print(f"\nFound {len(df)} high-quality opportunities across {len(WATCHLIST)} tickers.")
else:
    print("No opportunities met criteria in the current chain.")

# Optional: Recent news for headline sentiment check
print("\n--- Recent News (check against your .docx for sentiment) ---")
for ticker in WATCHLIST[:5]:  # limit for speed
    try:
        news = list(client.list_ticker_news(ticker, limit=2))
        if news:
            print(f"{ticker}: {news[0].title} ({news[0].publisher})")
    except:
        pass
