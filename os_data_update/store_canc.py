import pandas as pd

from helpers import *


def update_canc(epoc_last_updated):
    path = "csvs/all_canc.csv"
    all_canc = pd.read_csv(path)

    for i in range(0, 50000):
        print(i)
        events = get_canc(i, epoc_last_updated)

        try:
            assets_events = events["asset_events"]
        except:
            print("d")

        if len(assets_events) == 0:
            break

        for a in assets_events:
            df = parse_ape_canc(a)
            if df.empty == False:
                if all_canc[all_canc.canc_event_id == df.canc_event_id.item()].empty:
                    all_canc = all_canc.append(df)

    try:
        all_canc.to_csv(path)
        return "done"
    except Exception as e:
        return e
