import pandas as pd
from datetime import datetime, timedelta

from helpers import *

"""
TODO
    1. implement transfer events
    2. check listing types for expire
    
    DONE - filter for the correct listing types
"""

# check to make sure ape listing is not canc or sold
def is_still_listed(ape):
    ape_id = ape.ape_id.item()

    ape_canc = recent_canc[recent_canc.ape_id == ape_id]
    ape_sale = all_sales[all_sales.ape_id == ape_id]

    if ape_canc.empty:
        has_canc = False
    else:
        has_canc = ape_canc.canc_event_time.item() > ape.listing_event_time.item()

    if ape_sale.empty:
        has_sold = False
    else:
        has_sold = ape_sale.sale_time.item() > ape.listing_event_time.item()

    if has_canc or has_sold:
        return False
    else:
        return True


##get all os data
all_apes = pd.read_csv("csvs/all_the_apes.csv")
all_listings = pd.read_csv("csvs/all_listings.csv")
all_sales = pd.read_csv("csvs/all_sales.csv")
all_canc = pd.read_csv("csvs/all_canc.csv")

#filter listings
all_listings = all_listings[all_listings.auction_type != "english"]
all_listings = all_listings[all_listings.is_private == False]
all_listings.listing_event_time = all_listings.listing_event_time.astype("datetime64[ns]")

all_canc.canc_event_time = all_canc.canc_event_time.astype("datetime64[ns]")
all_sales.sale_time = all_sales.sale_time.astype("datetime64[ns]")

#join trait data to listings
all_listings = all_listings.merge(all_apes, left_on="ape_id", right_on="ape_id", how="left")

#only get most recent sale per ape
all_sales = all_sales.groupby("ape_id").apply(get_max_sales).reset_index(drop=True)

# only sales this month
all_sales = all_sales[all_sales.sale_time > datetime(2021, 10, 1)]

#join trait data to sales
all_sales = all_sales.merge(all_apes, left_on="ape_id", right_on="ape_id", how="left")

#only get most recent listing per ape
recent_listings = (all_listings.groupby("ape_id").apply(get_max_listing).reset_index(drop=True))

#only get most recent canc per ape
recent_canc = all_canc.groupby("ape_id").apply(get_max_canc).reset_index(drop=True)

# calcualtes the mean sale for a apes
total_mean = all_sales.sale_price.mean()

#used to store output
good_listings = pd.DataFrame()

#TODO expand this to all traits
# loops through each mouth trait
for mouth in all_sales.Mouth.unique():

    #find the cheepest listing for that trait
    cheapest_listing = (
        recent_listings[recent_listings.Mouth == mouth]
        .sort_values(by="listing_price", ascending=True)
        .reset_index()
    )

    #search through listings starting with the lowest
    for index, row in cheapest_listing.iterrows():
        listing = cheapest_listing.iloc[[index]]
        # need exception for transfer event
        if is_still_listed(listing):

            # calcualte the rarity of trair as %
            rarity_perc = (all_apes[all_apes.Mouth == mouth].shape[0] / 10000) * 100

            # mean sale of that trait
            mean = all_sales[all_sales.Mouth == mouth].sale_price.mean()

            # create a object with trait, rarity and diff from avg
            df_mouth = {
                "mouth": mouth,
                "mean": mean,
                "diff": mean - total_mean,
                "rarity": rarity_perc,
                "ape_id": listing.ape_id.item(),
                "listing_price": listing.listing_price.item(),
            }


            print(df_mouth)
            good_listings = good_listings.append(df_mouth, ignore_index=True)
            break

    print(good_listings)
