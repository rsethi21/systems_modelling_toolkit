from parse import parse_interactions, parse_substrates, parse_rates
from network import Network

import pandas as pd
import numpy as np
import json
import pdb


if __name__ == "__main__":
    interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/interactions.csv")
    substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/substrates.csv")
    rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/rates.csv")
    n = Network("network_original", rates, substrates, interactions)

    time = np.linspace(0,500,num=10001)
    for s in n.substrates.keys():
        print(f"{s} = {n.represent_rate(51, s)}")
    # n.load_adapter("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/adapter.json")
    # y = n.y(time)
    # n.graph(y, time)
    arguments = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/fitting_parameters.json"))
    data = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/fit_data.json"))
    n.fit(time, data, arguments, path="/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_original/adapter.json", number=10, mlp=4)