from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
import json
from src.ai.tools.financials import get_metrics

router = APIRouter()
REPORT_METRICS = ["revenue", "net_income", "net_profit_margin", "return_on_assets",
                  "return_on_equity" , "free_cash_flow"]

@router.get("/v1/companies/{ticker}")
async def get_company_financial(ticker):
        try:
                df = await run_in_threadpool(get_metrics,ticker,REPORT_METRICS)
        except Exception:
                raise HTTPException(status_code=502, detail="Financial data source unavailable.")   
                 
        if df.empty:
                raise HTTPException(status_code=401, detail=f"No data found for {ticker.upper()}.")
        df[REPORT_METRICS] = df[REPORT_METRICS].astype(float)
        result = json.loads(
                df.to_json(
                        orient="records",
                        date_format="iso"
                )
        )
        return {
                "ticker" : ticker.upper(),
                "result" : result
        }