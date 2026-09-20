# AlphaLake – Phase 1

## Goal

Build a Spark-based financial data pipeline that ingests
public-company financial statements and transforms them into
analytics-ready company fundamentals.

## Initial companies

MSFT
AAPL
GOOGL
AMZN
NVDA

## Input data

Income statement
Balance sheet
Cash-flow statement

## Bronze output

Raw API/XBRL responses stored without business transformations.

## Silver output

Normalized financial statement records.

## Gold output

One record per company per fiscal year containing:

- revenue
- revenue growth
- gross profit
- operating income
- operating margin
- net income
- total assets
- total debt
- shareholders' equity
- operating cash flow
- capital expenditure
- free cash flow
- ROE
- debt-to-equity