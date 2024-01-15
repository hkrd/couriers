RATE_CARDS = {
    "bronze_tier": {
        "hourly_minimum": 14.50,
        "successful_attempt": 0.459,
        "unsuccessful_attempt": 0.229,
        "long_route_bonus": {"amount": 10.00, "min_successful_drops": 30},
        "loyalty_bonus_routes": {"amount": 20.00, "min_routes": 10},
    },
    "silver_tier": {
        "hourly_minimum": 13.50,
        "successful_attempt": 0.65,
        "unsuccessful_attempt": 0.00,
        "loyalty_bonus_attempts": {"amount": 19.00, "min_attempts": 150},
        "quality_bonus": {
            "amount": 25.00,
            "min_success_rate": 97.0,
            "min_attempts": 20,
        },
    },
    "gold_tier": {
        "hourly_minimum": 15.00,
        "successful_attempt": 0.511,
        "unsuccessful_attempt": 0.126,
        "consistency_bonus": {
            "amount": 32.00,
            "min_success_rate": 96.5,
            "min_routes": 2,
        },
    },
    "platinum_tier": {
        "hourly_minimum": 15.25,
        "successful_attempt": 0.667,
        "unsuccessful_attempt": 0.155,
        "long_route_bonus": {
            "amount": 12.00,
            "min_successful_drops": 30,
        },  # Same as bronze_tier
        "loyalty_bonus_attempts": {
            "amount": 18.00,
            "min_attempts": 150,
        },  # Same as silver_tier
        "consistency_bonus": {
            "amount": 34.50,
            "min_success_rate": 96.5,
            "min_routes": 2,
        },  # Same as gold_tier
    },
}
