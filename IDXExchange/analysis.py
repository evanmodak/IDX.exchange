import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Directory where all monthly CSV files are stored
DATA_DIR = os.path.expanduser("~/Applications/IDXExchange/")

# Date range: Jan 2024 → last completed month
start = datetime(2024, 1, 1)
end = datetime.today().replace(day=1) - relativedelta(months=1)

# Build list of year/month strings e.g. ["202401", "202402", ...]
months = []
cursor = start
while cursor <= end:
    months.append(f"{cursor.year}{cursor.month:02d}")
    cursor += relativedelta(months=1)

# Load and concatenate all monthly files
listing_frames = []
sold_frames = []

for ym in months:
    listing_frames.append(pd.read_csv(os.path.join(DATA_DIR, f"CRMLSListing{ym}.csv")))
    sold_frames.append(pd.read_csv(os.path.join(DATA_DIR, f"CRMLSSold{ym}.csv")))

listings = pd.concat(listing_frames, ignore_index=True)
sold = pd.concat(sold_frames, ignore_index=True)

# Row counts BEFORE filter
print(f"Listings before filter: {len(listings)}")
print(f"Sold before filter:     {len(sold)}")

# Filter to Residential properties only
listings = listings[listings["PropertyType"] == "Residential"]
sold = sold[sold["PropertyType"] == "Residential"]

# Row counts AFTER filter
print(f"Listings after filter:  {len(listings)}")
print(f"Sold after filter:      {len(sold)}")

# Save combined datasets
listings.to_csv(os.path.join(DATA_DIR, "listings_residential_combined.csv"), index=False)
sold.to_csv(os.path.join(DATA_DIR, "sold_residential_combined.csv"), index=False)

print("Done! Files saved.")