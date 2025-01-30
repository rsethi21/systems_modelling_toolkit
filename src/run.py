from parse import parse_interactions, parse_substrates, parse_rates
from network import Network

import pandas as pd
import numpy as np
import json
import pdb


if __name__ == "__main__":
    interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/interactions_expanded.csv")
    substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/substrates_expanded.csv")
    rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/rates_expanded.csv")
    n = Network("network_original", rates, substrates, interactions)

    time = np.linspace(0,500,num=10001)
    for s in n.substrates.keys():
        print(f"{s} = {n.represent_rate(51, s)}")
    
    
    n.load_adapter("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/adapter.json")
    y = n.y(time, steady_state_fold_normalization=True)
    n.store_track(y, "/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/current_fit.csv")
    n.graph(y, time, path="./figure_literature", substrates_to_plot=["pAKT", "pPTEN", "GSK3B", "LPS"], ylim_lower=0, ylim_higher=2)
    
    
    # arguments = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/fitting_parameters.json"))
    # data = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/fit_data_expanded.json"))
    # n.fit(time, data, arguments, path="/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten/adapter_expanded.json", number=10, mlp=4)
