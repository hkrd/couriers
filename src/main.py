from fastapi import FastAPI, HTTPException
from .models import ActivityLog, EarningsStatement
from .earnings_calculator import calculate_earnings
from .rate_cards import RATE_CARDS
from typing import List

app = FastAPI()


@app.post("/earnings/{rate_card_id}", response_model=EarningsStatement)
async def compute_earnings(rate_card_id: str, activity_log: List[ActivityLog]):
    if rate_card_id not in RATE_CARDS:
        raise HTTPException(status_code=404, detail="Rate card not found")
    return calculate_earnings(activity_log, rate_card_id)
