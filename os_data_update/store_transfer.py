import pandas as pd
from pandas.core.indexes.api import all_indexes_same

from helpers import *


def update_transfer(epoc_last_updated):
    path = "csvs/all_transfers.csv"
    all_transfers = pd.read_csv(path)

    #all_transfers = pd.DataFrame()

    for i in range(0, 50000):
        print(i)
        events = get_transfers(i, epoc_last_updated)

        try:
            assets_events = events["asset_events"]
        except:
            assets_events = []

        if len(assets_events) == 0:
            break

        for a in assets_events:
            df = parse_ape_transfer(a)
            if df.empty == False:
                if all_transfers[all_transfers.transfer_event_id == df.transfer_event_id.item()].empty:
                # only apped if id is not already stored
                    all_transfers = all_transfers.append(df)

    try:
        all_transfers.to_csv(path)
        return "done"
    except Exception as e:
        return e
