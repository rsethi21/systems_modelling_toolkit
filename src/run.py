from parse import parse_interactions, parse_substrates, parse_rates
from network import Network

import pandas as pd
import numpy as np
import pdb

if __name__ == "__main__":
    interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/interactions.csv")
    substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/substrates.csv")
    rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/rates.csv")
    n = Network("network_test", rates, substrates, interactions)

    time = np.linspace(0,500,num=10001)
    y = n.y(time)
    n.graph(y, time)