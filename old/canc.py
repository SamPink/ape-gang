import numpy
import pandas as pd
from pandas._libs.tslibs import NaT

from helpers import *

"""
TODO
    1. it would be more efficient to read all events at the same time, then sort them into time order and drop duplicates per apes
"""

# get all apes with listings
listings = pd.read_csv("csvs/all_listings.csv")
listings.listing_event_time = listings.listing_event_time.astype("datetime64[ns]")
# listings.ape_id = listings.ape_id.split("#")[1]
last_updated = pd.read_csv("csvs/lastUpdated.csv")
epoc_last_updated = last_updated.lastUpdated.item()


# loop throuh all canc events
for i in range(0, 5000):
    print(i)
    try:
        canc = get_canc(i)

        if len(canc["asset_events"]) == 0:
            break
    except Exception as e:
        print(e)

    for c in canc["asset_events"]:
        df = parse_ape_canc(c)
        
        if df.empty == False:
            ape_id = df.ape_id.item()
            # convert canc event to dataframe

            df["canc_event_time"] = df["canc_event_time"].astype("datetime64[ns]")

            # look for ape in listings
            ape_listing = listings.loc[listings["ape_id"].isin(df.ape_id)]
            ape_listing_id = ape_listing.index.item()

            # if canc is after most recent listing
            if pd.notnull(ape_listing.listing_event_time.item()):
                if df.canc_event_time.item() > ape_listing.listing_event_time.item():
                    # remove listing
                    print(f"delisted {ape_listing.ape_id.item()}")
                    print(f"delist time {df.canc_event_time.item()}")
                    print(f"list time {ape_listing.listing_event_time.item()}")
                    print("\n")

                    listings.at[ape_listing_id, "listing_price"] = None
                    listings.at[ape_listing_id, "listing_event_id"] = None
                    listings.at[ape_listing_id, "listing_event_time"] = None

        else:
            print("Done")

# listings.to_csv('csvs/apes_with_listings_updated.csv')

print(listings)
