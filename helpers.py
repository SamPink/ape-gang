import requests
import pandas as pd

base = "https://api.opensea.io/api/v1/"
slug = "ape-gang"


def parse_id(a):
    ape_id = a.get("asset").get("name")
    return ape_id.split("#")[1]


def parse_ape(a):
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

    ape =  {
        "ape_id": a.get("asset").get("name"),
        "sale_price": (int(a.get("total_price")) / 1000000000000000000),
        "sale_time": a.get("created_date"),
    }

    return pd.DataFrame(ape, index=[0])


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

def get_events(i):
    url = f"{base}events?collection_slug={slug}d&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_sales(i):
    url = f"{base}events?collection_slug={slug}&event_type=successful&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_canc(i, epoc_last_updated):
    url_canc = f"{base}events?collection_slug={slug}&event_type=cancelled&only_opensea=false&&occurred_after={epoc_last_updated}&offset={i*50}&limit=50"
    response = requests.request("GET", url_canc)
    return response.json()["asset_events"]
