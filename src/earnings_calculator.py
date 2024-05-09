from typing import List
from src.models import ActivityLog, EarningsStatement, LineItem
from src.rate_cards import RATE_CARDS
from datetime import datetime
from decimal import Decimal
from collections import defaultdict, Counter


def make_naive(dt: datetime) -> datetime:
    """Convert an offset-aware datetime to offset-naive."""
    return dt.replace(tzinfo=None) if dt.tzinfo else dt


def get_amount(bonus: str, rate_card: dict):
    if bonus in rate_card:
        return Decimal(rate_card[bonus]["amount"])
    return Decimal(0)


def get_bonus_slug(name):
    bonuses_slugs = {
        "Long route bonus": "long_route_bonus",
        "Loyalty bonus (routes)": "loyalty_bonus_routes",
        "Loyalty bonus (attempts)": "loyalty_bonus_attempts",
        "Quality bonus": "quality_bonus",
        "Consistency bonus": "consistency_bonus",
    }
    return bonuses_slugs[name]


def calculate_hours_worked(activity_log: List[ActivityLog]) -> float:
    route_times = defaultdict(lambda: {"start": datetime.max, "end": datetime.min})
    for log in activity_log:
        route_id = log.route_id
        attempt_time = make_naive(log.attempt_date_time)
        route_times[route_id]["start"] = min(
            route_times[route_id]["start"], attempt_time
        )
        route_times[route_id]["end"] = max(route_times[route_id]["end"], attempt_time)

    total_seconds = sum(
        [
            (route["end"] - route["start"]).total_seconds()
            for route in route_times.values()
        ]
    )
    return total_seconds / 3600  # Convert seconds to hours


def calculate_earnings(
    activity_log: List[ActivityLog], rate_card_id: str
) -> EarningsStatement:
    if rate_card_id not in RATE_CARDS:
        raise ValueError(f"Rate card with ID '{rate_card_id}' not found.")

    rate_card = RATE_CARDS[rate_card_id]
    successful_attempts = sum(log.success for log in activity_log)
    unsuccessful_attempts = len(activity_log) - successful_attempts
    hours_worked = calculate_hours_worked(activity_log)

    # Initialize earnings
    line_items = []
    total_earnings = Decimal(
        successful_attempts * rate_card["successful_attempt"]
    ) + Decimal(unsuccessful_attempts * rate_card["unsuccessful_attempt"])

    # Correctly count attempts for line items
    line_items.append(
        LineItem(
            name="Per successful attempt",
            quantity=successful_attempts,
            rate=Decimal(rate_card["successful_attempt"]),
            total=Decimal(successful_attempts * rate_card["successful_attempt"]),
        )
    )
    line_items.append(
        LineItem(
            name="Per unsuccessfuly attempt",
            quantity=unsuccessful_attempts,
            rate=Decimal(rate_card["unsuccessful_attempt"]),
            total=Decimal(unsuccessful_attempts * rate_card["unsuccessful_attempt"]),
        )
    )

    # Initialize bonus conditions
    long_route_bonus_earned = False
    loyalty_bonus_routes_earned = False
    loyalty_bonus_attempts_earned = False
    quality_bonus_earned = False
    consistency_bonus_earned = False

    # Calculate bonuses based on rate card
    route_counter = Counter(log.route_id for log in activity_log if log.success)
    success_rate = successful_attempts / len(activity_log) if activity_log else 0

    if rate_card_id == "bronze_tier":
        if any(
            count > rate_card["long_route_bonus"]["min_successful_drops"]
            for count in route_counter.values()
        ):
            long_route_bonus_earned = True

        if len(route_counter) >= rate_card["loyalty_bonus_routes"]["min_routes"]:
            loyalty_bonus_routes_earned = True

    elif rate_card_id == "silver_tier":
        if successful_attempts >= rate_card["loyalty_bonus_attempts"]["min_attempts"]:
            loyalty_bonus_attempts_earned = True

        if (
            success_rate >= rate_card["quality_bonus"]["min_success_rate"] / 100
            and successful_attempts >= rate_card["quality_bonus"]["min_attempts"]
        ):
            quality_bonus_earned = True

    elif rate_card_id == "gold_tier":
        if (
            success_rate >= rate_card["consistency_bonus"]["min_success_rate"] / 100
            and len(route_counter) >= rate_card["consistency_bonus"]["min_routes"]
        ):
            consistency_bonus_earned = True

    elif rate_card_id == "platinum_tier":
        long_route_bonus_earned = any(
            count > rate_card["long_route_bonus"]["min_successful_drops"]
            for count in route_counter.values()
        )
        loyalty_bonus_attempts_earned = (
            successful_attempts >= rate_card["loyalty_bonus_attempts"]["min_attempts"]
        )
        consistency_bonus_earned = (
            success_rate >= rate_card["consistency_bonus"]["min_success_rate"] / 100
            and len(route_counter) >= rate_card["consistency_bonus"]["min_routes"]
        )

    # Add all bonuses to line items
    bonuses = [
        (
            "Long route bonus",
            get_amount("long_route_bonus", rate_card),
            long_route_bonus_earned,
        ),
        (
            "Loyalty bonus (routes)",
            get_amount("loyalty_bonus_routes", rate_card),
            loyalty_bonus_routes_earned,
        ),
        (
            "Loyalty bonus (attempts)",
            get_amount("loyalty_bonus_attempts", rate_card),
            loyalty_bonus_attempts_earned,
        ),
        ("Quality bonus", get_amount("quality_bonus", rate_card), quality_bonus_earned),
        (
            "Consistency bonus",
            get_amount("consistency_bonus", rate_card),
            consistency_bonus_earned,
        ),
    ]

    for bonus_name, bonus_amount, earned in bonuses:
        if get_bonus_slug(bonus_name) in rate_card:
            line_items.append(
                LineItem(
                    name=bonus_name,
                    quantity=1 if earned else 0,
                    rate=bonus_amount,
                    total=bonus_amount if earned else 0,
                )
            )
            total_earnings += bonus_amount if earned else 0

    # Apply hourly minimum earnings
    hourly_minimum_earnings = Decimal(rate_card["hourly_minimum"] * hours_worked)
    if total_earnings < hourly_minimum_earnings:
        hourly_minimum_amount = hourly_minimum_earnings - total_earnings
        line_items.append(
            LineItem(
                name="Hourly Minimum Top-up",
                quantity=0,
                rate=hourly_minimum_amount,
                total=hourly_minimum_amount,
            )
        )
        total_earnings = hourly_minimum_earnings

    # Calculate line items subtotal and create EarningsStatement
    line_items_subtotal = sum(item.total for item in line_items)
    earnings_statement = EarningsStatement(
        line_items=line_items,
        line_items_subtotal=line_items_subtotal,
        hours_worked=hours_worked,
        minimum_earnings=hourly_minimum_earnings,
        final_earnings=total_earnings,
    )

    return earnings_statement
