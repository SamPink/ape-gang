import pandas as pd

from helpers import *

all_listings = pd.DataFrame()

for i in range(0, 50000):
    print(i)
    events = get_listings(i)

    try:
        assets_events = events["asset_events"]
    except:
        print("d")

    if len(assets_events) == 0:
        break

    for a in assets_events:
        df = parse_ape_listing(a)
        all_listings = all_listings.append(df)

print(all_listings)
all_listings.to_csv("all_listings2.csv")
