import numpy
import pandas as pd
from helpers import *
from os_data_update.store_canc import update_canc
from os_data_update.store_listings import update_listings
from os_data_update.store_sales import update_sales


#test

# get all apes with listings
listings = pd.read_csv("csvs/all_listings.csv")
listings.listing_event_time = listings.listing_event_time.astype("datetime64[ns]")
epoc_last_updated = listings.listing_event_time.max().value


listings = update_listings(epoc_last_updated)

canc = update_canc(epoc_last_updated)

sales = update_sales(epoc_last_updated)

if listings == "done" and sales == "done" and canc == "done":
    last_updated = pd.read_csv("csvs/lastUpdated.csv")
    last_updated.at[0, "lastUpdated"] = epoc_last_updated
    last_updated.to_csv("csvs/lastUpdated.csv")

    print("updated!")

else:
    print("fucekd it")
