# UPI Payment Failure Intelligence System

## 🚀 Live Dashboard

**[Click here to see the interactive dashboard](https://upi-payment-failure-analysis-gm4t7n7vaucbsezgqvd6ho.streamlit.app/)**

The dashboard is fully interactive — explore bank corridors, time windows, merchants, and failure reasons.

---

## What's the problem?

So I was thinking — every day billions of UPI transactions happen. But some fail. And when they fail, merchants lose money, customers get frustrated, and nobody really knows which bank pairs or time windows are the actual problem.

I decided to analyze this. Find the real patterns. Put a number on how much money is being lost.

## What I built

A data analysis system that answers 3 questions:
1. Which bank corridors (sender bank → receiver bank) have weirdly high failure rates?
2. Which time of day do failures spike?
3. Which merchant types are hit hardest?

## How it works

**Data layer:** SQLite database with 50,000 UPI transactions with realistic patterns
**Analysis layer:** SQL queries that group failures by corridor, time, and merchant type
**Visualization:** Interactive dashboard built with Streamlit where you can explore patterns

## Key findings

- **Yes Bank → HDFC corridor** fails 24.5% of the time. That's 2x the platform average. Equals ₹10.65 Lakhs monthly loss.
- **Midnight to 6 AM** accounts for ₹147 Lakhs damage — one-third of all losses. Probably because bank servers run at reduced capacity.
- **Food Delivery** category has most failures because of micro-transactions hitting bank minimum thresholds.

## Files in this repo

- `upi_analysis.sql` — all the SQL queries I used to analyze the data
- `app.py` — the Streamlit dashboard code
- `upi_project.db` — SQLite database with 50K transactions
- `requirements.txt` — Python dependencies

## How to use this

If you want to run it locally:

```bash
pip install streamlit pandas matplotlib
streamlit run app.py
```

Then open the dashboard and explore the data by clicking tabs.

## What I learned

- How to think about business problems, not just code problems
- Window functions in SQL (RANK, PERCENT_RANK for comparing each corridor to average)
- How to convert percentages to rupee damage so business people actually care
- Why reference lines in charts matter — they show you what normal is, then you see what's abnormal

## Why this matters for a recruiter

At Razorpay or PhonePe, this is exactly the kind of analysis the payments team does. They need to know which corridors are broken, which times are bad, which merchants to watch. This project shows I can:
- Write SQL that actually answers questions
- Think about business impact, not just numbers
- Build something a non-technical person can use
- Find insights that matter

## If I had more time

I'd add:
- Predictive model to forecast failures 24 hours ahead
- Automated alerts for corridors crossing a failure threshold
- A/B testing framework to test fixes
- Integration with actual NPCI data

But right now this shows the core skill — finding the problem and proving it with data.

---

Built by me while learning data analysis. Questions? Reach out.
