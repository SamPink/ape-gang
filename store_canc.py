import numpy
import pandas as pd
from pandas._libs.tslibs import NaT

from helpers import *

all_canc = pd.DataFrame()

for i in range(0, 50000):
    print(i)
    events = get_canc(i)

    try:
        assets_events = events["asset_events"]
    except:
        print("d")

    if len(assets_events) == 0:
        break

    for a in assets_events:
        df = parse_ape_canc(a)
        all_canc = all_canc.append(df)

print(all_canc)
all_canc.to_csv("all_canc.csv")
