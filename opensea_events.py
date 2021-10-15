from numpy import e
import requests
import pandas as pd

from parseApe import parse_ape_data

all_apes = pd.read_csv("apes_with_listings.csv")

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
        "ape_id": parse_id(a),
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


listing = pd.DataFrame()


for i in range(0, 5000):
    print(i)
    try:
        apes = get_listings(i)
    except:
        print("done")
    for a in apes["asset_events"]:
        ape = parse_ape(a)
        if ape != None:
            listing = listing.append(ape, ignore_index=True)
        else:
            print("Done")

all_apes = all_apes.merge(
    listing, left_on="ape_id", right_on="ape_id", how="left", suffixes=("_1", "_2")
)

# check canc

# loop throuh all canc events
for i in range(0, 5000):
    print(i)
    try:
        canc = get_canc(i)
    except:
        print("done")
    for a in apes["asset_events"]:
        ape = parse_ape(a)
        if ape != None:
            listing = listing.append(ape, ignore_index=True)
        else:
            print("Done")
# if canc is after most recent listing

# removing listing

print(all_apes)

all_apes.to_csv("apes_with_listings.csv")
