import pandas as pd
from datetime import datetime, timedelta

from helpers import *

# import files
all_apes = pd.read_csv("csvs/all_the_apes.csv")
all_listings = pd.read_csv("all_listings2.csv")
all_sales = pd.read_csv("all_sales.csv")
all_canc = pd.read_csv("all_canc.csv")

#exclude english auctions
all_listings = all_listings[all_listings.auction_type != 'english']

# convert data types
all_listings.listing_event_time = all_listings.listing_event_time.astype(
    "datetime64[ns]"
)
all_canc.canc_event_time = all_canc.canc_event_time.astype("datetime64[ns]")
all_sales.sale_time = all_sales.sale_time.astype("datetime64[ns]")

# only sales this month
all_sales = all_sales[all_sales.sale_time > datetime(2021, 10, 1)]

# merge traits to apes
all_listings = all_listings.merge(
    all_apes, left_on="ape_id", right_on="ape_id", how="left"
)
all_sales = all_sales.merge(all_apes, left_on="ape_id", right_on="ape_id", how="left")

# only include most revent events per ape
all_listings = (
    all_listings.groupby("ape_id").apply(get_max_listing).reset_index(drop=True)
)
# all_canc = all_canc.groupby("ape_id").apply(get_max_canc).reset_index(drop=True)
all_sales = all_sales.groupby("ape_id").apply(get_max_sales).reset_index(drop=True)

for index, row in all_sales.iterrows():
    sale = all_sales.iloc[[index]]
    sale_price = sale.sale_price.item()
    sale_id = sale.ape_id.item()

    listing = all_listings[all_listings.ape_id == sale_id]

    if listing.empty == False:
        if listing.listing_event_time.item() > sale.sale_time.item():
            listing_price = listing.listing_price.item()

            if listing_price < sale_price:
                print(f"ape id: {sale_id} - last sale {sale_price} - listing price {listing_price}")
