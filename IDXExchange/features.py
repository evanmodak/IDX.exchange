import pandas as pd
import os as os

DATA_DIR = os.path.expanduser("~/Applications/IDXExchange/")

sold = pd.read_csv(os.path.join(DATA_DIR, "sold_cleaned.csv"), low_memory=False)

# Coerce types
for col in ["ClosePrice", "OriginalListPrice", "LivingArea", "DaysOnMarket"]:
    sold[col] = pd.to_numeric(sold[col], errors="coerce")
for col in ["CloseDate", "ListingContractDate", "PurchaseContractDate"]:
    sold[col] = pd.to_datetime(sold[col], errors="coerce")

# Engineered metrics
sold["price_ratio"] = sold["ClosePrice"] / sold["OriginalListPrice"]
sold["price_per_sqft"] = sold["ClosePrice"] / sold["LivingArea"]
sold["days_on_market"] = sold["DaysOnMarket"]
sold["close_year"] = sold["CloseDate"].dt.year
sold["close_month"] = sold["CloseDate"].dt.month
sold["close_yrmo"] = sold["close_year"] * 100 + sold["close_month"]
sold["listing_to_contract_days"] = (sold["PurchaseContractDate"] - sold["ListingContractDate"]).dt.days
sold["contract_to_close_days"] = (sold["CloseDate"] - sold["PurchaseContractDate"]).dt.days

# Sample output
cols = ["ClosePrice", "OriginalListPrice", "LivingArea",
        "price_ratio", "price_per_sqft", "days_on_market",
        "close_year", "close_month", "close_yrmo",
        "listing_to_contract_days", "contract_to_close_days"]
print(sold[cols].dropna(subset=["price_ratio"]).head(10).to_string(index=False))

# Segmented summary by PropertyType
print(sold.groupby("PropertyType")[["price_ratio", "price_per_sqft", "days_on_market"]].mean().round(2))

sold.to_csv(os.path.join(DATA_DIR, "sold_engineered.csv"), index=False)
print("Done")
