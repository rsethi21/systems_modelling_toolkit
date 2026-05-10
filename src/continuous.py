import gradio as gr

from parse import parse_interactions, parse_substrates, parse_rates
from network import Network

import pandas as pd
import numpy as np
import json
import pdb
import os

time_set = 2499

def plot_tracks(n, time, conditions):
    for i, condition in enumerate(conditions):
        n.apply_stimuli(condition["stimuli"], condition["amt"], condition["time_range"])
        if condition["adapter"] != None:
            for rate_name, rate_value in condition["adapter"].items():
                n.rates[rate_name].current_value = n.rates[rate_name].initial_value * rate_value
        if condition["apply"] == None:
            ybar = n.y(time, steady_state_fold_normalization=True)
        else:
            ybar = n.y(time, steady_state_fold_normalization=False, steady_state_fold_w_existing=condition["apply"])
        n.graph(ybar, time, path=f"./data/outputs/figure_literature_sep{condition['amt']}_{i}.png", substrates_to_plot=["pAKT", "pPTEN", "pGSK3B", "LPS", "ATP", "LY294002", "Ca"], xlim_lower=720, xlim_higher=time_set+1, ylim_lower = 0, ylim_higher=2)
        n.store_track(ybar, time, condition["path"])
        n.reset_stimuli()
        if condition["adapter"] != None:
            for rate_name, rate_value in condition["adapter"].items():
                n.rates[rate_name].current_value = n.rates[rate_name].initial_value

interactions = parse_interactions("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/interactions_expanded.csv")
substrates = parse_substrates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/substrates_expanded.csv")
rates = parse_rates("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/rates_expanded.csv")
n = Network("network_original", rates, substrates, interactions)
resolution = 10000
time = np.linspace(0,time_set,num=resolution)
for s in n.substrates.keys():
    print(f"{s} = {n.represent_rate(279, s)}")
n.load_adapter("/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/pi3k_pten_totals/adapter_expanded_modified.json")
folder = "/home/rsethi1/school_rsh/PKH/systems_modelling_toolkit/data/outputs"
stimuli = [n.substrates[name] for name in n.order if n.substrates[name].substrate_type=="stimulus"]

def run_experiment(folder_name, stimuli):
    path = os.join(folder, folder_name)
    if folder_name not in os.listdir(folder):
        os.system[f"mkdir {path}"]
    substrates = n.order
    conditions = {

    }
    plot_tracks(n, time, conditions)

demo = gr.Interface(
    fn=run_experiment,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()