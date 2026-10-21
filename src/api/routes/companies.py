from fastapi import APIRouter
import json
from ...ai.tools.financials import get_financial_report_databricks

router = APIRouter()


@router.get("/companies/{ticker}")
async def get_company_financial(ticker):
        df = get_financial_report_databricks(ticker=ticker)
        df["revenue"] = df["revenue"].astype(float)
        df["net_income"] = df["net_income"].astype(float)
        df["net_profit_margin"] = df["net_profit_margin"].astype(float)
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