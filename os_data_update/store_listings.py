import pandas as pd

from helpers import *


def update_listings(epoc_last_updated):
    path = "csvs/all_listings.csv"

    all_listings = pd.read_csv(path)

    for i in range(0, 50000):
        print(i)
        events = get_listings(i, epoc_last_updated)

        try:
            assets_events = events["asset_events"]
        except:
            print("d")

        if len(assets_events) == 0:
            break

        for a in assets_events:
            df = parse_ape_listing(a)
            if df.empty == False:
                if all_listings[
                    all_listings.listing_event_id == df.listing_event_id.item()
                ].empty:
                    all_listings = all_listings.append(df)
    try:
        all_listings.to_csv(path)
        return "done"
    except Exception as e:
        return e
