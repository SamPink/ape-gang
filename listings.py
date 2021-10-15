import pandas as pd

from helpers import *

all_apes = pd.read_csv("csvs/all_the_apes.csv")

listing = pd.DataFrame()

for i in range(0, 5000):
    print(i)
    try:
        apes = get_listings(i)
    except:
        print("")
    for a in apes["asset_events"]:
        ape = parse_ape(a)
        if ape != None:
            listing = listing.append(ape, ignore_index=True)
        else:
            print("Done")

all_apes = all_apes.merge(
    listing, left_on="ape_id", right_on="ape_id", how="left", suffixes=("_1", "_2")
)


all_apes.to_csv("csvs/apes_with_listings.csv")