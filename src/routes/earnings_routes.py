from fastapi import APIRouter, HTTPException
from src.models import ActivityLog, EarningsStatement
from src.earnings_calculator import calculate_earnings
from src.rate_cards import RATE_CARDS
from typing import List

router = APIRouter()

@router.post("/earnings/{rate_card_id}", response_model=EarningsStatement)
async def compute_earnings(rate_card_id: str, activity_log: List[ActivityLog]):
    if rate_card_id not in RATE_CARDS:
        raise HTTPException(status_code=404, detail="Rate card not found")
    return calculate_earnings(activity_log, rate_card_id)