import pandas as pd

from helpers import *

all_apes = pd.read_csv("csvs/all_the_apes.csv")

sales = pd.DataFrame()

"""
TODO


DONE
    when joining, need to prevent multiple being added
"""

for i in range(0, 5000):
    print(i)
    try:
        sales = get_sales(i)

        if sales.get("asset_events") == None:
            break
    except:
        print("")

    for a in sales["asset_events"]:
        ape = parse_ape_sale(a)

        if ape != None:
            if listing.empty == False:
                # check to see if listing is already stored for ape
                if listing[listing.ape_id == ape.get("ape_id")].empty == False:
                    # skip are 2nd listing must be older
                    continue

                listing = listing.append(ape, ignore_index=True)
            else:
                listing = listing.append(ape, ignore_index=True)

all_apes = all_apes.merge(
    listing, left_on="ape_id", right_on="ape_id", how="left", suffixes=("_1", "_2")
)

all_apes.to_csv("csvs/apes_with_listings.csv")
