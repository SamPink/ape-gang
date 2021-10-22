
from helpers import *
import pandas as pd

# traits: Clothes, Ears, Hat, Fur, Mouth, Eyes

def get_good_listings(trait, ape_data):
    """
    gets good listings, depending on their trait using the ape data
    """
    # print(ape_data)
    for ape_with_trait in ape_data.get("all_sales")[trait].unique():
        
        #find the cheepest listing for that trait
        cheapest_listing = (
            ape_data.get("recent_listings")[ape_data.get("recent_listings")[trait] == ape_with_trait]
            .sort_values(by="listing_price", ascending=True)
            .reset_index()
        )

        #search through listings starting with the lowest
        for index, row in cheapest_listing.iterrows():
            listing = cheapest_listing.iloc[[index]]
            # need exception for transfer event
            if is_still_listed(listing, ape_data):

                # calcualte the rarity of trair as %
                rarity_perc = (ape_data.get("all_apes")[ape_data.get("all_apes")[trait] == ape_with_trait].shape[0] / 10000) * 100

                # mean sale of that trait
                mean = ape_data.get("all_sales")[ape_data.get("all_sales")[trait] == ape_with_trait].sale_price.mean()

                # create a object with trait, rarity and diff from avg
                df_trait = {
                    trait: ape_with_trait,
                    "mean": mean,
                    "diff": mean - ape_data.get("total_mean"),
                    "rarity": rarity_perc,
                    "ape_id": listing.ape_id.item(),
                    "listing_price": listing.listing_price.item(),
                }


                # print(df_trait)
                ape_data["good_listings"][trait] = ape_data["good_listings"][trait].append(df_trait, ignore_index=True)
                # print(ape_data["good_listings"][trait])
                
                break
    # get good listings for trait
    print(ape_data["good_listings"][trait].head())
        


# check to make sure ape listing is not canc or sold
def is_still_listed(ape, ape_data):
    ape_id = ape.ape_id.item()

    ape_canc = ape_data.get("recent_canc")[ape_data.get("recent_canc").ape_id == ape_id]
    ape_sale = ape_data.get("all_sales")[ape_data.get("all_sales")["ape_id"] == ape_id]

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