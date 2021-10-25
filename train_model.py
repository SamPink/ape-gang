import pandas as pd
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from helpers import *


"""
trains model based on sales, writes model to file
"""


def train_model():

    # import sales data
    sales = pd.read_csv("./csvs/all_sales.csv")
    sales.sale_time = sales.sale_time.astype("datetime64[ns]")

    sales = sales[["ape_id", "sale_price", "sale_time"]]
    sales = sales[sales["sale_price"] > 0.01]

    sales["day"] = sales["sale_time"].dt.date
    # sales_by_date = sales.groupby("day").count().sale_price

    sales = sales.join(
        sales.groupby("day").median().sale_price, rsuffix="_daily_avg", on="day"
    )

    sales["price_diff"] = sales.sale_price - sales.sale_price_daily_avg

    # filter to recent sales
    sales = sales[sales.sale_time > dt.datetime(2021, 9, 1)]

    # get ape trait data
    apes = pd.read_csv("./csvs/apes_dummy_values.csv")

    # join trair data to sales
    df = sales.merge(apes, on="ape_id", how="left")

    df = df.drop(
        columns=[
            "ape_id",
            "sale_time",
            "day",
            "Unnamed: 0",
            "sale_price",
            "sale_price_daily_avg",
        ]
    )

    x = df.drop(columns="price_diff")
    y = df["price_diff"]

    # create train test split for x and y
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)

    # persist model in memory
    dump(rf, "./models/randomforest.joblib")


"""
get dummines on all ape data then store the data
"""


def get_dummines_all_apes():
    apes = pd.read_csv("./csvs/all_the_apes.csv")

    apes["trait_n"] = apes[["Clothes", "Ears", "Hat", "Fur", "Mouth", "Eyes"]].count(
        axis=1
    )

    df = pd.get_dummies(
        apes[
            [
                "Clothes",
                "Ears",
                "Hat",
                "Fur",
                "Mouth",
                "Eyes",
                "trait_n",
                "ape_id",
            ]
        ],
        columns=["Clothes", "Ears", "Hat", "Fur", "Mouth", "Eyes", "trait_n"],
    )

    df.to_csv("./csvs/apes_dummy_values.csv")


train_model()
# get_dummines_all_apes()
