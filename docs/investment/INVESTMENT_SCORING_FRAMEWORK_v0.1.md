# Investment Scoring Framework v0.1

## Lesson Learned

A single market-wide buy score is insufficient for portfolio decisions. Buy attractiveness and risk must be evaluated per asset, and long-, medium-, and short-term horizons must be separated before producing an overall score.

## Core Decision Axes

1. **Long-term score** — structural quality, earnings growth, competitive position, valuation, financial resilience, long-term trend/catalysts.
2. **Medium-term score** — earnings revisions, industry cycle, institutional/foreign flows, medium-term trend, catalysts/events, valuation change.
3. **Short-term score** — price momentum, flow changes, volume/capital inflow, distance from highs, relative strength, near-term events.
4. **Risk score** — price/volatility risk, business risk, financial risk, event risk, liquidity risk, macro risk, and incremental portfolio risk.
5. **Position suitability** — converts attractiveness and risk into an actionable capital-allocation decision.

## Initial Horizon Weights

- Long term: **50%**
- Medium term: **30%**
- Short term: **20%**

`Overall Buy Score = 0.50 × Long + 0.30 × Medium + 0.20 × Short`

These weights are **initial hypotheses, not permanent rules**. They must be validated against observed decisions and outcomes before being promoted to a stable governance rule.

## High-Value Additional Factors

The research identified six additions with high expected decision value:

- Expectation gap / what is already priced in
- Fundamental direction rather than only fundamental level
- Catalyst strength and time-to-catalyst
- Financial/business resilience
- Liquidity and transaction-cost risk
- Incremental portfolio risk / concentration and factor overlap

## Important Separation

Do not collapse everything into one score too early:

- **Buy Score:** How attractive is adding the asset now?
- **Risk Score:** How severe is the downside/uncertainty if the thesis is wrong?
- **Position Suitability:** How much capital is appropriate given attractiveness, risk, and existing portfolio exposure?

A high buy score with high risk can justify a smaller position; a lower buy score with low risk can justify waiting rather than selling.

## Decision Interpretation

The framework must distinguish:

- Good asset / bad entry
- Good asset / good entry
- Tactical opportunity / weak long-term thesis
- Strong thesis / temporary short-term weakness
- Attractive asset / excessive portfolio concentration

## Guardrails

- Do not use currency moves as a standalone buy signal.
- Do not treat price momentum as proof of fundamental improvement.
- Do not treat valuation as a standalone timing signal.
- Do not infer broad risk-on from a single asset class.
- Do not increase position size solely because the composite score is high when portfolio concentration is already excessive.

## Next Validation Work

1. Define 0–100 scoring rubrics for every factor.
2. Define evidence freshness requirements by horizon.
3. Test whether factor scores add information beyond price momentum.
4. Backtest horizon weights and sensitivity to alternative weights.
5. Compare composite-score decisions against actual forward outcomes.
6. Record false-positive and false-negative cases before changing weights.

## Status

**v0.1 — research hypothesis. Not yet a production investment rule.**
