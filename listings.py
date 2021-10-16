import pandas as pd

from helpers import *

all_apes = pd.read_csv("csvs/all_the_apes.csv")

listing = pd.DataFrame()

"""
TODO
    1. when joining, need to prevent multiple being added
"""

for i in range(0, 5000):
    print(i)
    try:
        apes = get_listings(i)

        if apes.get("asset_events") == None:
            break
    except:
        print("")

    for a in apes["asset_events"]:
        ape = parse_ape(a)

        if ape != None:
            if listing.empty == False:
                # check to see if listing is already sotred for ape
                if listing[listing.ape_id == ape.get("ape_id")].empty == False:
                    # drop previous listing
                    listing = listing[listing.ape_id != ape.get("ape_id")]

                listing = listing.append(ape, ignore_index=True)
            else:
                listing = listing.append(ape, ignore_index=True)

all_apes = all_apes.merge(
    listing, left_on="ape_id", right_on="ape_id", how="left", suffixes=("_1", "_2")
)


all_apes.to_csv("csvs/apes_with_listings.csv")
