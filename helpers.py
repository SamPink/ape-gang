import requests

base = "https://api.opensea.io/api/v1/"
slug = "ape-gang"


def parse_id(a):
    ape_id = a.get("asset").get("name")
    return ape_id.split("#")[1]


def parse_ape(a):
    if a.get("asset") == None:
        return None

    return {
        "ape_id": parse_id(a),
        "listing_event_id": a.get("id"),
        "listing_event_time": a.get("created_date"),
        "listing_price": (int(a.get("starting_price")) / 1000000000000000000),
    }


def parse_ape_canc(a):
    if a.get("asset") == None:
        return None

    return {
        "ape_id": a.get("asset").get("name"),
        "canc_event_id": a.get("id"),
        "canc_event_time": a.get("created_date"),
    }

def get_listings(i):
    url = f"{base}events?collection_slug={slug}&event_type=created&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url)
    return response.json()


def get_canc(i):
    url_canc = f"{base}events?collection_slug={slug}&event_type=cancelled&only_opensea=false&offset={i*50}&limit=50"
    response = requests.request("GET", url_canc)
    return response.json()["asset_events"]
