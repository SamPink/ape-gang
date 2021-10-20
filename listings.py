import pandas as pd

from helpers import *

# all_apes = pd.read_csv("csvs/all_the_apes.csv")
listings = pd.read_csv("csvs/apes_with_listings.csv")

listings["listing_event_time"] = pd.to_datetime(listings["listing_event_time"])

epoc_last_updated = listings.listing_event_time.max().value

listing = pd.DataFrame()

"""
TODO


DONE
    when joining, need to prevent multiple being added
"""

for i in range(0, 1000):
    print(i)
    try:
        apes = get_listings(i, epoc_last_updated)

        if len(apes['asset_events']) == 0:
            break

    except Exception as e:
        print(e)

    for a in apes["asset_events"]:
        df = parse_ape(a)

        if df.empty == False:
            print(df.listing_event_time)
            ape_listing = listings.loc[listings["ape_id"].isin(df.ape_id)]
            ape_listing_id = ape_listing.index.item()

            listings.at[ape_listing_id, "listing_price"] = df.listing_price.item()
            listings.at[ape_listing_id, "listing_event_id"] = df.listing_event_id.item()
            listings.at[ape_listing_id, "listing_event_time"] = df.listing_event_time.item()


listings.to_csv("csvs/apes_with_listings.csv")

last_updated = pd.DataFrame({"lastUpdated": epoc_last_updated}, index=[0])
last_updated.to_csv("csvs/lastUpdated.csv")
