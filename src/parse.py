import pandas as pd
import numpy as np
from rate import Rate
from substrate import Substrate
from interaction import Interaction

def fill_nas(df):
    for i, row in df.iterrows():
        for col in df.columns:
            if pd.isna(df.loc[i,col]) or np.nan == df.loc[i,col]:
                df.loc[i,col] = None

# same comments for the other functions below
def parse_rates(rates_csv_path):
    rates_df = pd.read_csv(rates_csv_path, index_col=0) # read csv
    fill_nas(rates_df) # fill na values for blanks
    rates_dictionary = {v: None for v in rates_df.name.values} # convert to dictionary
    # iterate rates and and create a dictionary of rate objects
    for _, rate in rates_df.iterrows():
        inputs = rate.to_dict()
        rates_dictionary[inputs["name"]] = Rate(**inputs)
    rates_dictionary["zero"] = Rate(**{"name": "zero", "value": 0.0, "upper_bound": 0.0, "lower_bound": 0.0, "bound_type": "real", "fixed": True})
    return rates_dictionary

def parse_substrates(substrates_csv_path):
    substrates_df = pd.read_csv(substrates_csv_path, index_col=0)
    fill_nas(substrates_df)
    substrates_dictionary = {v: None for v in substrates_df.name.values}
    for _, substrate in substrates_df.iterrows():
        inputs = substrate.to_dict()
        inputs = {n: v for n, v in inputs.items() if not pd.isna(v)}
        substrates_dictionary[inputs["name"]] = Substrate(**inputs)
    return substrates_dictionary

def parse_interactions(interactions_csv_path):
    interactions_df = pd.read_csv(interactions_csv_path, index_col=0)
    fill_nas(interactions_df)
    interactions_dictionary = {v: None for v in interactions_df.name.values}
    for _, interaction in interactions_df.iterrows():
        inputs = interaction.to_dict()
        interactions_dictionary[inputs["name"]] = Interaction(**inputs)
    return interactions_dictionary