import numpy
import pandas as pd
from pandas._libs.tslibs import NaT

from helpers import *

# get all apes with listings
listings = pd.read_csv("csvs/all_the_apes.csv")

# loop throuh all canc events
for i in range(0, 5000):
    print(i)
    try:
        events = get_events(i)
    except Exception as e:
        print(e)
    for event in events:
        print(event)
        #df = parse_ape_canc(c)
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
