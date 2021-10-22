import pandas as pd

from helpers import *


def update_sales(epoc_last_updated):
    path = "csvs/all_sales.csv"
    all_sales = pd.read_csv(path)

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

    try:
        all_sales.to_csv(path)
        return "done"
    except Exception as e:
        return e
