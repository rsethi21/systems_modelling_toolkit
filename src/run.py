from parse import parse_interactions, parse_substrates, parse_rates
from network import Network

import pandas as pd
import numpy as np
import json
import pdb


def plot_tracks(n, time, conditions):
    for condition in conditions:
        n.apply_stimuli(condition["stimuli"], condition["amt"], condition["time_range"])
        y = n.y(time, steady_state_fold_normalization=False)
        n.store_track(y, time, condition["path"])
        n.reset_stimuli()

if __name__ == "__main__":
    interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/interactions_expanded.csv")
    substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/substrates_expanded.csv")
    rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/rates_expanded.csv")
    experiments = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/experiments.json"))
    n = Network("network_original", rates, substrates, interactions)

    resolution = 10000
    time = np.linspace(0,999,num=resolution)
    for s in n.substrates.keys():
        print(f"{s} = {n.represent_rate(279, s)}")
    
    
    n.load_adapter("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/adapter_expanded.json")
    plot_tracks(n, time, experiments)

    # y = n.y(time, steady_state_fold_normalization=True)
    # n.store_track(y, time, "/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/current_fit_atp.csv")
    # n.graph(y, time, path="./figure_literature", substrates_to_plot=["pAKT", "pPTEN", "GSK3B", "LPS"], ylim_lower=0, ylim_higher=2)
    
    
    # arguments = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/fitting_parameters.json"))
    # data = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/fit_data_expanded.json"))
    # n.fit(time, data, arguments, path="/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/adapter_expanded.json", number=10, mlp=4)
