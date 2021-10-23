import pandas as pd
from datetime import datetime, timedelta

from helpers import *
from traits import get_good_listings
"""
TODO
    1. implement transfer events
    2. check listing types for expire
    
    DONE - filter for the correct listing types
"""

def get_all_ape_data():
    """
    Gets all the ape data and returns it in a dictionary
    """

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
    # print(all_sales.head())
    #only get most recent listing per ape
    recent_listings = (all_listings.groupby("ape_id").apply(get_max_listing).reset_index(drop=True))

    #only get most recent canc per ape
    recent_canc = all_canc.groupby("ape_id").apply(get_max_canc).reset_index(drop=True)

    # calcualtes the mean sale for a apes
    total_mean = all_sales.sale_price.mean()

    # create dict for good listings
    good_listings = {}
    # dict to store all ape dataframes
    ape_data = {}

    # list of all traits
    traits = ["Clothes", "Ears", "Hat", "Fur", "Mouth", "Eyes"]

    # loop through each trait and create df
    for trait in traits:
        good_listings[trait] = pd.DataFrame()

    # print(good_listings)
    # call to func to get best listings for a specfic trait

    ape_data["traits"] = traits
    ape_data["all_sales"] = all_sales
    ape_data["all_apes"] = all_apes
    ape_data["all_canc"] = all_canc
    ape_data["all_listings"] = all_listings
    ape_data["recent_listings"] = recent_listings
    ape_data["recent_canc"] = recent_canc
    ape_data["total_mean"] = total_mean
    ape_data["good_listings"] = good_listings

    return ape_data

def get_good_listings_per_trait(ape_data):
    """
    Calls get good listings for each trait
    """
    for trait in ape_data["traits"]:
        get_good_listings(trait, ape_data)
        # write each good listing for each trait to a csv file
        ape_data["good_listings"][trait].to_csv(".\csvs\\good_apes_by_trait\\" + trait + "_good_listings.csv")



def main():
    ape_data = get_all_ape_data()
    get_good_listings_per_trait(ape_data)

if __name__ == "__main__":
    main()
    
