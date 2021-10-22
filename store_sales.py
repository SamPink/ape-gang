import numpy
import pandas as pd
from pandas._libs.tslibs import NaT

from helpers import *

last_updated = pd.read_csv("csvs/lastUpdated.csv")
epoc_last_updated = last_updated.lastUpdated.item()

all_sales = pd.read_csv("csvs/all_sales.csv")

for i in range(0, 50000):
    print(i)
    events = get_sales(i, epoc_last_updated)

    try:
        assets_events = events["asset_events"]
    except:
        print("d")

    if len(assets_events) == 0:
        break

    for a in assets_events:
        df = parse_ape_sale(a)
        if df.empty == False:
            if all_sales[all_sales.sale_id == df.sale_id.item()].empty:
                # only apped if id is not already stored
                all_sales = all_sales.append(df)

print(all_sales)
all_sales.to_csv("all_sales.csv")
