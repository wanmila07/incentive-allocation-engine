import pandas as pd
import numpy as np

np.random.seed(42)
n = 5352

# Business name generator
prefixes = ["Warung", "Kedai", "Restoran", "Perniagaan", "Gerai", "Bengkel", "Kedai Runcit"]
names = ["Maju", "Bahagia", "Sejahtera", "Murah", "Jaya", "Damai", "Makmur", "Setia", "Murni", "Indah"]
suffixes = [str(i).zfill(3) for i in range(1, n+1)]

import random
random.seed(42)
business_names = [f"{random.choice(prefixes)} {random.choice(names)} {suffixes[i]}" for i in range(n)]

df = pd.DataFrame({
    "business_name": business_names,
    "idstd": np.random.randint(1200000, 1400000, n),
    "owner_age": np.random.randint(20, 70, n),
    "owner_female": np.random.choice([0, 1], n, p=[0.42, 0.58]),
    "owner_education": np.random.choice([1,2,3,4,5,6], n, p=[0.03,0.15,0.19,0.44,0.10,0.09]),
    "hh_vulnerability": np.random.uniform(0, 1, n),
    "sector_experience": np.random.randint(1, 40, n),
    "mgmt_practices_index": np.random.uniform(0, 1, n),
    "social_capital": np.random.uniform(0, 1, n),
    "push_entrepreneur": np.random.uniform(0, 1, n),
    "employment_regular": np.random.randint(1, 6, n),
    "revenue_regular_usd": np.random.exponential(500, n).clip(50, 15000),
    "business_age": np.random.randint(1, 30, n),
    "sector_food": np.random.choice([0, 1], n, p=[0.44, 0.56]),
    "location_type": np.random.choice([1,2,3,4], n),
    "formality_status": np.zeros(n, dtype=int),
    "technology_index": np.random.uniform(0, 1, n),
    "operating_intensity": np.random.uniform(0, 1, n),
    "recordkeeping_index": np.random.uniform(0, 1, n),
    "has_loan": np.random.choice([0, 1], n, p=[0.89, 0.11]),
    "collateral_proxy": np.random.uniform(0, 1, n),
    "income_stable": np.random.uniform(0, 1, n),
    "financial_literacy_proxy": np.random.uniform(0, 1, n),
    "regulatory_barriers": np.random.uniform(0, 1, n),
    "institutional_quality": np.random.uniform(0, 1, n),
    "market_infrastructure": np.random.uniform(0, 1, n),
    "performance_index": np.random.uniform(0, 1, n),
    "formalization_readiness": np.random.uniform(0, 1, n),
    "resilience_proxy": np.random.uniform(0, 1, n),
})

# Generate scores
df["efficiency_score"] = (
    0.4 * (df["revenue_regular_usd"] / df["revenue_regular_usd"].max() * 100) +
    0.3 * (df["mgmt_practices_index"] * 100) +
    0.3 * (df["operating_intensity"] * 100)
).round(4)

df["equity_score"] = (
    0.4 * (df["hh_vulnerability"] * 100) +
    0.3 * (df["owner_female"] * 100) +
    0.3 * ((1 - df["owner_education"] / 6) * 100)
).round(4)

df["sustainability_score"] = (
    0.4 * (df["technology_index"] * 100) +
    0.3 * (df["sector_experience"] / 40 * 100) +
    0.3 * (df["resilience_proxy"] * 100)
).round(4)

# Dominant objective
scores = df[["efficiency_score", "equity_score", "sustainability_score"]]
mapping = {0: "Efficiency", 1: "Equity", 2: "Multi-Objective"}
df["dominant_objective"] = scores.idxmax(axis=1).map({
    "efficiency_score": "Efficiency",
    "equity_score": "Equity",
    "sustainability_score": "Sustainability"
})

df.to_csv("data/processed/scored_dataset.csv", index=False)
print(f"Synthetic dataset generated: {df.shape}")
print(df[["efficiency_score","equity_score","sustainability_score","dominant_objective"]].describe())