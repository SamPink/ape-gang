import pandas as pd
from datetime import datetime, timedelta

from helpers import *

"""
TODO
    1. implement transfer events
    2. check listing types for expire
    
    DONE - filter for the correct listing types https://opensea.io/assets/0x495f947276749ce646f68ac8c248420045cb7b5e/4981676894159712808201908443964193325271219637660871887967791658715116994561
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


all_apes = pd.read_csv("csvs/all_the_apes.csv")

all_listings = pd.read_csv("all_listings2.csv")

all_listings = all_listings[all_listings.auction_type != "english"]
all_listings = all_listings[all_listings.is_private == False]

all_listings.listing_event_time = all_listings.listing_event_time.astype(
    "datetime64[ns]"
)

all_canc = pd.read_csv("all_canc.csv")
all_canc.canc_event_time = all_canc.canc_event_time.astype("datetime64[ns]")

all_listings = all_listings.merge(
    all_apes, left_on="ape_id", right_on="ape_id", how="left"
)


all_sales = pd.read_csv("all_sales.csv")
all_sales.sale_time = all_sales.sale_time.astype("datetime64[ns]")

all_sales = all_sales.groupby("ape_id").apply(get_max_sales).reset_index(drop=True)

# only sales this month
all_sales = all_sales[all_sales.sale_time > datetime(2021, 10, 1)]


all_sales = all_sales.merge(all_apes, left_on="ape_id", right_on="ape_id", how="left")

recent_listings = (
    all_listings.groupby("ape_id").apply(get_max_listing).reset_index(drop=True)
)

recent_canc = all_canc.groupby("ape_id").apply(get_max_canc).reset_index(drop=True)

# calcualtes the mean sale for a ape mouths
total_mean = all_sales.sale_price.mean()

df_mouth = pd.DataFrame()

# loops through each mouth trait
for mouth in all_sales.Mouth.unique():

    # calcualte the rarity of trair as %
    rarity_perc = (all_apes[all_apes.Mouth == mouth].shape[0] / 10000) * 100

    # mean sale of that trait
    mean = all_sales[all_sales.Mouth == mouth].sale_price.mean()

    # create a object with trait, rarity and diff from avg
    df_mouth = df_mouth.append(
        {
            "mouth": mouth,
            "mean": mean,
            "diff": mean - total_mean,
            "rarity": rarity_perc,
        },
        ignore_index=True,
    )

    cheapest_listing = recent_listings[recent_listings.Mouth == mouth].sort_values(
        by="listing_price", ascending=True
    ).reset_index()

    for index, row in cheapest_listing.iterrows():
        listing = cheapest_listing.iloc[[index]]
        # need exception for transfer event
        if is_still_listed(listing):
            print(listing)
            print(mouth)
            break
