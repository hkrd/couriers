## Couriers
App to calculate the earnings of each courier doing deliveries based on which 'Delivery Tier' they are on, determining their earnings based on success rate of deliveries and bonuses.

Tech Stack:

Python 3.9+
FastAPI,
Pydantic,
Docker

run with ```uvicorn src.main:app  --reload```
run tests with ```poetry run pytest```

Deployed on ```https://couriers-rndb.onrender.com/docs```

Usage

Use with any of the tiers: ```bronze_tier, silver_tier, gold_tier, platinum_tier``` and example payload:

```
[
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
      "success": true
    },
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:37:11.897203+00:00",
      "success": true
    },
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:39:10.938613+00:00",
      "success": true
    },
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:43:14.747595+00:00",
      "success": false
    },
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:45:45.375317+00:00",
      "success": true
    },
    {
      "route_id": "RT5QHQ6M3A937H",
      "attempt_date_time": "2023-12-18T08:45:58.396736+00:00",
      "success": true
    }
  ]
```