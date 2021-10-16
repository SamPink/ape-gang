import numpy
import pandas as pd
from pandas._libs.tslibs import NaT

from helpers import *

# get all apes with listings
listings = pd.read_csv("csvs/apes_with_listings.csv")
# listings.ape_id = listings.ape_id.split("#")[1]
listings["listing_event_time"] = listings["listing_event_time"].astype("datetime64[ns]")


# loop throuh all canc events
for i in range(0, 5000):
    print(i)
    try:
        canc = get_canc(i)
    except:
        print("done")
    for c in canc:
        ape = parse_ape_canc(c)
        if ape != None:
            ape_id = ape.get("ape_id")
            # convert canc event to dataframe
            df = pd.DataFrame(ape, index=[0])

            df["canc_event_time"] = df["canc_event_time"].astype("datetime64[ns]")

            # look for ape in listings
            ape_listing = listings.loc[listings["ape_id"].isin(df.ape_id)]

            # if canc is after most recent listing
            if pd.notnull(ape_listing.listing_event_time.item()):
                if df.canc_event_time.item() > ape_listing.listing_event_time.item():
                    print("hey")

            # remove listing
        else:
            print("Done")
