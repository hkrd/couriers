from pydantic import BaseModel
from datetime import datetime
from typing import List


class LineItem(BaseModel):
    name: str
    rate: float
    total: float


class ActivityLog(BaseModel):
    route_id: str
    attempt_date_time: datetime
    success: bool


class EarningsStatement(BaseModel):
    line_items: List[LineItem]
    line_items_subtotal: float
    hours_worked: float
    minimum_earnings: float
    final_earnings: float
