from parse import parse_interactions, parse_substrates, parse_rates
from network import Network
import pandas as pd
import numpy as np
import json

interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/interactions_expanded.csv")
substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/substrates_expanded.csv")
rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/rates_expanded.csv")
experiments = json.load(open("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/pten_experiments.json"))
n = Network("network_original", rates, substrates, interactions)
resolution = 10000
time = np.linspace(0,1499,num=resolution)
n.load_adapter("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/adapter_expanded_modified.json")
n.apply_stimuli(["LY294002"], [1.0], [[500,700]])
y = n.y(time, steady_state_fold_normalization=True)
n.graph(y, time, ylim_lower=0, ylim_higher=2)
n.store_track(y, time, "test.csv")