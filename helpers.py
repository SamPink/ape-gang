import requests
import pandas as pd

base = "https://api.opensea.io/api/v1/"
slug = "ape-gang"


def parse_id(a):
    ape_id = a.get("asset").get("name")
    return ape_id.split("#")[1]


def parse_ape_listing(a):
    if a.get("asset") == None:
        return pd.DataFrame()

    ape = {
        "ape_id": a.get("asset").get("name"),
        "listing_event_id": a.get("id"),
        "listing_event_time": a.get("created_date"),
        "listing_price": (int(a.get("starting_price")) / 1000000000000000000),
    }

    return pd.DataFrame(ape, index=[0])


def parse_ape_sale(a):
    if a.get("asset") == None:
        return None

    buyer_name = a.get("winner_account").get("user")
    if buyer_name != None:
        buyer_name = buyer_name.get("username", None)
    
    seller_name = a.get("seller").get("user")
    if seller_name != None:
        seller_name.get("username", None)
    ape = {
        "sale_id": a.get("id"),
        "ape_id": a.get("asset").get("name"),
        "sale_price": (int(a.get("total_price")) / 1000000000000000000),
        "sale_time": a.get("created_date"),
        "seller_name": seller_name,
        "seller_wallet": a.get("seller").get("address"),
        "buyer_name": buyer_name,
        "buyer_wallet": a.get("winner_account").get("address"),
    }

    return pd.DataFrame(ape, index=[0])


def parse_ape_offer(a):
    if a.get("asset") == None:
        return None

    return {
        "event_type": a.get("event_type"),
        "ape_id": a.get("asset").get("name"),
        "event_id": a.get("id"),
        "event_time": a.get("created_date"),
        "offer_amount": int(a.get("bid_amount")) / (1000000000000000000),
    }


def parse_ape_canc(a):
    if a.get("asset") == None:
        return None

    ape = {
        "ape_id": a.get("asset").get("name"),
        "canc_event_id": a.get("id"),
        "canc_event_time": a.get("created_date"),
    }

    return pd.DataFrame(ape, index=[0])


def get_listings(i, epoc_last_updated):
    url = f"{base}events?collection_slug={slug}&event_type=created&only_opensea=false&occurred_after={epoc_last_updated}&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_listings(i):
    url = f"{base}events?collection_slug={slug}&event_type=created&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_events(i):
    url = f"https://api.opensea.io/api/v1/events?collection_slug=ape-gang&only_opensea=false&offset=0&limit=50"
    response = requests.request("GET", url)
    return response.json()["asset_events"]


def get_sales(i):
    url = f"{base}events?collection_slug={slug}&event_type=successful&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_canc(i):
    url_canc = f"{base}events?collection_slug={slug}&event_type=cancelled&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url_canc)
    return response.json()
