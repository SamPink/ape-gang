import streamlit as st
import pandas as pd
import numpy as np


st.title('Some cool ape visualisations')

def load_rarity_data():
    values = {}
    for i in range(1,7):
        values[f"{i}T_apes"] = pd.read_csv(f".\\csvs\\apes_by_trait_count\\{i}T_rar_apes.csv")
    return values
