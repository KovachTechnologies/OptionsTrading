# Options Credit Spread Strategies for Level-Based Trading

*A reference for short-timeframe (intraday to 3-day) directional and range-bound theses on futures options (ZN, ES, GC, CL) via Interactive Brokers.*

> **Disclaimer:** This document is for educational purposes only and does not constitute financial advice. Interactive Brokers is referenced as the account platform of choice; strategy mechanics apply generally to any broker offering defined-risk spread orders.

---

## Overview

All three strategies below share a common design goal: **defined maximum risk at trade entry.** Each is built from two options of the same type (calls or puts) and the same expiration, at different strikes. Because one leg is bought and one is sold, the combined position has a capped, known loss regardless of how far price moves against the thesis — there is no need to actively manage the position to avoid open-ended drawdown, which is the central appeal for short-duration, level-based trading.

All three structures here are entered as **net credit** trades: the premium received for the leg sold exceeds the premium paid for the leg bought, so the trader collects cash upfront. This aligns time decay (theta) with the trade — a meaningful consideration even over a 1–3 day hold, since it means the passage of time works in the trader's favor as long as the thesis holds, rather than against it as it does with a debit structure.

---

## 1. Bull Credit Spread (Bull Put Spread) — for Trending-Up / Support-Holding Markets

### Definition
A bull credit spread is constructed by **selling a put** at a strike near or below the expected support/pivot level, and **buying a put** at a lower strike as protection. The trade is entered for a net credit.

- Sell put at strike **A** (higher strike, closer to money)
- Buy put at strike **B** (lower strike, further out of the money)
- A > B, same expiration

### Thesis Fit
Used when the trader expects a level to act as a **floor** — i.e., the "support holds" or "pivot and rally" scenarios. The trade does not require the underlying to actually rally; it only requires the underlying to stay above the short strike (A) through expiration.

### Risk/Reward Profile
| Metric | Formula | Outcome Condition |
|---|---|---|
| Max gain | Net credit received | Price finishes at/above strike A |
| Max loss | (Width between strikes) − (net credit received) | Price finishes at/below strike B |
| Breakeven | Strike A − net credit received | — |

### Pros
- Defined, capped risk known before entry.
- Profits even if price stays flat or drifts modestly higher — does not require the rally to actually happen, only that the floor holds.
- Positive theta: time decay benefits the position while the thesis is intact.
- Requires less precision than a debit spread, since being "roughly right" about the floor is sufficient.

### Cons
- Capped upside — no benefit from a large rally beyond the credit collected.
- Max loss can still be a meaningful percentage of capital at risk if the width is wide relative to the credit.
- A sharp, fast break of the lower strike near expiration can move quickly to max loss due to elevated gamma in short-dated options.

### Worked Example
**Thesis:** Underlying is expected to pivot off $100 and hold as support, with an anticipated move toward $105.

- Sell $100 put for $2.00 (collect $200)
- Buy $95 put for $0.50 (pay $50)
- **Net credit received:** $1.50 ($150 per spread)

**Outcomes:**
- **Max gain:** $150 — if price finishes at/above $100 at expiration
- **Max loss:** $5.00 width − $1.50 credit = $3.50 ($350) — if price finishes at/below $95
- **Breakeven:** $100 − $1.50 = **$98.50**

---

## 2. Bear Credit Spread (Bear Call Spread) — for Trending-Down / Rejection Markets

### Definition
A bear credit spread is constructed by **selling a call** at a strike near or above the expected resistance/rejection level, and **buying a call** at a higher strike as protection. The trade is entered for a net credit.

- Sell call at strike **A** (lower strike, closer to money)
- Buy call at strike **B** (higher strike, further out of the money)
- A < B, same expiration

### Thesis Fit
Used when the trader expects a level to act as a **ceiling** — i.e., the "rejection at resistance" scenario. The trade does not require an actual selloff; it only requires the underlying to stay below the short strike (A) through expiration.

### Risk/Reward Profile
| Metric | Formula | Outcome Condition |
|---|---|---|
| Max gain | Net credit received | Price finishes at/below strike A |
| Max loss | (Width between strikes) − (net credit received) | Price finishes at/above strike B |
| Breakeven | Strike A + net credit received | — |

### Pros
- Defined, capped risk known before entry.
- Profits even if price stays flat or drifts modestly lower — does not require the selloff to actually happen, only that the ceiling holds.
- Positive theta: time decay benefits the position while the thesis is intact.
- Mirrors the bull credit spread mechanically, simplifying mental modeling for traders working both directions.

### Cons
- Capped upside — no benefit from a large selloff beyond the credit collected.
- Max loss can still be significant relative to credit if strikes are widely spaced.
- A sharp breakout through the upper strike near expiration can move quickly to max loss due to gamma risk in short-dated contracts.

### Worked Example
**Thesis:** Underlying is expected to reject $100 as resistance, with an anticipated selloff toward $95.

- Sell $100 call for $2.00 (collect $200)
- Buy $105 call for $0.50 (pay $50)
- **Net credit received:** $1.50 ($150 per spread)

**Outcomes:**
- **Max gain:** $150 — if price finishes at/below $100 at expiration
- **Max loss:** $5.00 width − $1.50 credit = $3.50 ($350) — if price finishes at/above $105
- **Breakeven:** $100 + $1.50 = **$101.50**

---

## 3. Iron Condor — for Ranging Markets

### Definition
An iron condor combines a bull put credit spread (below the range) and a bear call credit spread (above the range) in a single position, both sold against the same expiration. It is inherently a net credit strategy.

- Sell put at strike **A**, buy put at strike **B** (B < A) — put spread below the range
- Sell call at strike **C**, buy call at strike **D** (D > C) — call spread above the range
- B < A < C < D

### Thesis Fit
Used when the trader expects price to remain **contained** within a band — neither breaking down through the lower boundary nor breaking out above the upper boundary through expiration. This is the only one of the three strategies that is non-directional by design.

### Risk/Reward Profile
| Metric | Formula | Outcome Condition |
|---|---|---|
| Max gain | Total net credit received (both spreads combined) | Price finishes between strikes A and C |
| Max loss | (Width of the breached side) − (total net credit received) | Price finishes at/below B or at/above D |
| Lower breakeven | Strike A − total net credit | — |
| Upper breakeven | Strike C + total net credit | — |

### Pros
- Defined, capped risk on both sides of the range simultaneously.
- Profits from the passage of time and from range-bound chop — does not require any directional move at all.
- Two premium sources (put side + call side) typically produce a larger credit than a single-direction credit spread of comparable width, improving the risk/reward ratio for a correct range thesis.

### Cons
- The most capital-inefficient of the three in terms of margin, since risk exists on both sides even though only one side can be breached at a time.
- A breakout in either direction converts the position from a working range trade into a directional loser, and because two spreads are open simultaneously, adjusting or closing early can be more operationally complex than a single-direction spread.
- Requires a genuinely two-sided view (a real ceiling *and* a real floor) rather than a single-level thesis, so it is only appropriate when both boundaries are independently well-supported by the trader's read of the market.

### Worked Example
**Thesis:** Underlying is expected to range between $95 and $105 through expiration.

- Sell $95 put for $1.20, buy $90 put for $0.40 → credit $0.80 (put side)
- Sell $105 call for $1.20, buy $110 call for $0.40 → credit $0.80 (call side)
- **Total net credit received:** $1.60 ($160 per spread)

**Outcomes:**
- **Max gain:** $160 — if price finishes anywhere between $95 and $105 at expiration
- **Max loss:** $5.00 width (on the breached side) − $1.60 credit = $3.40 ($340) — if price finishes at/below $90 or at/above $110
- **Lower breakeven:** $95 − $1.60 = **$93.40**
- **Upper breakeven:** $105 + $1.60 = **$106.60**

---

## Summary Comparison

| Strategy | Directional View | Entry | Max Gain | Max Loss | Theta Bias |
|---|---|---|---|---|---|
| Bull Credit Spread (Bull Put) | Support holds / pivot up | Net credit | Credit received | Width − credit | Favorable |
| Bear Credit Spread (Bear Call) | Resistance holds / pivot down | Net credit | Credit received | Width − credit | Favorable |
| Iron Condor | Range holds (two-sided) | Net credit | Total credit received | Width − total credit (worse side) | Favorable |

### General Notes for Short-Timeframe (0–3 Day) Application
- **Strike width selection** is the primary lever for tuning risk/reward: narrower widths reduce both max loss and max gain; wider widths increase both. Width should be chosen based on a realistic assessment of how far price could move if the level thesis fails, not set arbitrarily.
- **Liquidity and execution quality** matter disproportionately at short time horizons — wide bid-ask spreads on far-dated or thinly traded strikes can erode the credit received before the position even has a chance to work.
- **Entering after level confirmation** (e.g., a visible bounce, rejection wick, or a session where price has already respected the range) rather than pre-positioning ahead of the level reduces exposure to being wrong about the level itself, since the position is only opened once the market has already begun to show the expected behavior.
