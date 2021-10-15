import pandas as pd

from helpers import *

#get all apes with listings
listings = pd.read_csv('csvs/apes_with_listings.csv')
#listings.ape_id = listings.ape_id.split("#")[1]
listings['listing_event_time'] = listings['listing_event_time'].astype('datetime64[ns]')


# loop throuh all canc events
for i in range(0, 5000):
    print(i)
    try:
        canc = get_canc(i)
    except:
        print("done")
    for c in canc:
        ape = parse_ape_canc(c)
        if ape != None:
            df = pd.DataFrame(ape, index=[0])
            df['canc_event_time'] = df['canc_event_time'].astype('datetime64[ns]')
            ape_listing = listings.loc[listings['ape_id'].isin(df.ape_id)]
        else:
            print("Done")
# if canc is after most recent listing