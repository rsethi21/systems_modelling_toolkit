from interaction import Interaction
import pandas as pd
import numpy as np
from scipy.integrate import odeint
from geneticalgorithm2 import geneticalgorithm2 as ga
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tqdm import tqdm
import pdb
import random

class Network:
    def __init__(self, name: str, rates_dictionary: dict, substrates_dictionary: dict, interactions_dictionary: dict):
        # create all necessary items and a preset order of substrates to normalize all operations
        self.name = name
        self.rates = rates_dictionary
        self.substrates = substrates_dictionary
        self.interactions = interactions_dictionary
        self.order = list(self.substrates.keys())

    def calculate_rate(self, t, substrate_name):
        # calculate base rates
        base_contribution_positive, base_contribution_negative = Interaction.calculate_base_contributions(self.substrates[substrate_name], self.substrates)
        # create by rate interactions
        effect_by_rate = {
                self.substrates[substrate_name].activation_rate: {
                    "effect": 1, 
                    "terms": [base_contribution_positive]
                },
                self.substrates[substrate_name].deactivation_rate: {
                    "effect": -1,
                    "terms": [base_contribution_negative]
                }
            }
        # find all relevant interactions
        effectors = [interaction for interaction in list(self.interactions.values()) if interaction.resultant == substrate_name]
        # iterate interactions and apply effects into dictionary
        for effector in effectors:
            # calculate contribution
            contribution = effector.calculate_contribution(self.substrates, self.rates)
            # apply to terms
            if effector.rate in list(effect_by_rate.keys()):
                effect_by_rate[effector.rate]["terms"].append(contribution)
            else:
                effect_by_rate[effector.rate] = {"effect": effector.effect, "terms": [contribution]}
        # apply rates from the dictionary assorted
        rate = 0
        for rate_name, output in effect_by_rate.items():
            temp_rate = self.rates[rate_name].current_value * output["effect"]
            for term in output["terms"]:
                temp_rate = temp_rate*term
            rate += temp_rate
        # check if substrate is within the bounds of active time range
        if self.substrates[substrate_name].active_time_ranges != None and np.nan != self.substrates[substrate_name].active_time_ranges:
            if self.substrates[substrate_name].active_time_ranges[0] <= t <= self.substrates[substrate_name].active_time_ranges[1]:
                if self.substrates[substrate_name].substrate_type != "stimulus":
                    return rate
                else:
                    if self.substrates[substrate_name].applied:
                        return rate
                    else:
                        return self.substrates[substrate_name].total_amt - self.substrates[substrate_name].current_value
            else:
                return 0
        else:
            if self.substrates[substrate_name].substrate_type == "stimulus":
                return 0
            else:
                return rate
    
    def dydt(self, y, time, parameter_sets=None):
        self.set_current_values(time, y)
        rates = []
        for s in self.order:
            rates.append(self.calculate_rate(time, s))
        return rates

    def y(self, times, parameter_sets=None):
        initials = self.get_initial_values()
        y = odeint(self.dydt, initials, times, args=(parameter_sets,))
        return y

    def y_distribution(self):
        pass

    def graph(self, y, time, path="./figure.png", random_state=0):
        colors = list(mcolors.CSS4_COLORS.keys())
        random.seed(random_state)
        random.shuffle(colors)
        fig = plt.figure()
        for i, substrate in tqdm(enumerate(self.order), desc="Plotting Each Substrate", total=len(self.order)):
            plt.plot(time, y[:,i], colors[i], label=self.substrates[substrate].name)
        plt.xlabel("Time (mins)",fontsize=12)
        plt.ylabel("Concentration (AU)",fontsize=12)
        plt.legend(loc="upper right", fontsize=5)
        fig.savefig(path)

    def graph_distribution(self):
        pass

    def represent_rate(self, t, substrate_name):
        # calculate base rates
        base_contribution_positive, base_contribution_negative = Interaction.represent_base_contribution(self.substrates[substrate_name])
        # create by rate interactions
        if self.substrates[substrate_name].substrate_type != "stimulus":
            effect_by_rate = {
                    self.substrates[substrate_name].activation_rate: {
                        "effect": 1, 
                        "terms": [base_contribution_positive]
                    },
                    self.substrates[substrate_name].deactivation_rate: {
                        "effect": -1,
                        "terms": [base_contribution_negative]
                    }
                }
        else:
            effect_by_rate = {
                    self.substrates[substrate_name].deactivation_rate: {
                        "effect": -1,
                        "terms": [base_contribution_negative]
                    }
                }
        # find all relevant interactions
        effectors = [interaction for interaction in list(self.interactions.values()) if interaction.resultant == substrate_name]
        # iterate interactions and apply effects into dictionary
        for effector in effectors:
            # calculate contribution
            contribution = effector.represent_contribution(self.substrates[effector.stimulus], self.rates)
            # apply to terms
            if effector.rate in list(effect_by_rate.keys()):
                effect_by_rate[effector.rate]["terms"].append(contribution)
            else:
                effect_by_rate[effector.rate] = {"effect": effector.effect, "terms": [contribution]}
        # apply rates from the dictionary assorted
        rate = ""
        for rate_name, output in effect_by_rate.items():
            if output["effect"] > 0:
                temp_rate = f"{rate_name}"
            else:
                temp_rate = f"-{rate_name}"
            for term in output["terms"]:
                temp_rate = temp_rate + f"[{term}]"
            if list(effect_by_rate.keys()).index(rate_name) != len(list(effect_by_rate.keys())) - 1:
                rate += f"{temp_rate} + "
            else:
                rate += f"{temp_rate}"
        # check if substrate is within the bounds of active time range
        if self.substrates[substrate_name].active_time_ranges != None and np.nan != self.substrates[substrate_name].active_time_ranges:
            if self.substrates[substrate_name].active_time_ranges[0] <= t <= self.substrates[substrate_name].active_time_ranges[1]:
                return rate
            else:
                return 0
        else:
            if self.substrates[substrate_name].substrate_type == "stimulus":
                return 0
            else:
                return rate

    def fit(self, times, data, arguments, initials=None, number=1, mlp=1):
        rates_to_fit = [r for r in list(self.rates.keys()) if not self.rates[r].fixed]
        bounds = [[self.rates[r].lower_bound, self.rates[r].upper_bound] for r in rates_to_fit]
        bound_types = [self.rates[r].bound_type for r in rates_to_fit]
        for i in range(len(bounds)):
            if bound_types[i] == "int":
                bounds[i] = [int(bounds[i][0]), int(bounds[i][1])]
        
        if initials == None:
            y0s = [] # instantiate empty list
            for _ in tqdm(range(number),desc="Generating Random Initial",total=number, disable=True): # iterate through the number of randomly generated intial conditions
                y0 = []
                for i, s in enumerate(self.order): # iterate through all the substrates
                    if self.substrates[s].substrate_type == "stimulus": # if the substrate is a stimulus category, use 0 for initial condition
                        y0.append(self.substrates[s].initial_value)
                    else:
                        y0.append(2**np.random.randn()) # else randomly generate one
                y0s.append(y0) # append sample conditions to a list of multiple random conditions
        else:
            y0s = initials

        def loss(X):
            self.reset_stimuli()
            self.set_current_rates(X, rates_to_fit)
            cost = 0
            count = 0
            for experiment in data:
                self.apply_stimuli(experiment["stimuli"], experiment["amts"], experiment["time_ranges"])
                predictions = self.y(times)
                for substrate_name, entries in experiment["data"].items():
                    index = self.order.index(substrate_name)
                    for entry in entries:
                        prediction = predictions[entry[0], index]
                        diff = prediction - entry[1]
                        cost += diff**2
                        count += 1
                self.reset_stimuli()
            return float(cost)/count
        pdb.set_trace()
        fitting_model = ga(function = loss,
                           dimension = len(bounds),
                           variable_type = bound_types,
                           variable_boundaries = bounds,
                           algorithm_parameters = arguments)
        fitting_model.run(set_function=ga.set_function_multiprocess(loss, n_jobs=mlp))

    def apply_stimuli(self, stimuli, amts, time_ranges):
        for stimulus, amt, time_range in zip(stimuli, amts, time_ranges):
            self.substrates[stimulus].total_amt = amt
            self.substrates[stimulus].active_time_ranges = time_range
            self.substrates[stimulus].applied = False

    def get_initial_values(self):
        return [self.substrates[substrate_name].initial_value for substrate_name in self.order] # return substrate values using the specific order

    def get_current_values(self):
        return [self.substrates[substrate_name].current_value for substrate_name in self.order] # return substrate values using the specific order

    def set_current_rates(self, new_values, names):
        for name, value in zip(names, new_values):
            self.rates[name].current_value = value

    def set_current_values(self, t, new_values):
        for i, substrate_name in enumerate(self.order): # following the same order
            if self.substrates[substrate_name].substrate_type == "stimulus":
                if self.substrates[substrate_name].active_time_ranges != None and np.nan != self.substrates[substrate_name].active_time_ranges:
                    if self.substrates[substrate_name].active_time_ranges[0] <= t <= self.substrates[substrate_name].active_time_ranges[1]:
                        if abs(self.substrates[substrate_name].current_value - self.substrates[substrate_name].total_amt) <= 0.01:
                            self.substrates[substrate_name].applied = True
                    else:
                        self.substrates[substrate_name].applied = False
            self.substrates[substrate_name].current_value >= self.substrates[substrate_name].total_amt
            self.substrates[substrate_name].current_value = new_values[i] # if not stimulus then just set to whatever the value is currently

    def reset_stimuli(self):
        for substrate_name in self.order:
            if self.substrates[substrate_name].substrate_type == "stimulus":
                self.substrates[substrate_name].total_amt = 0.0
                self.substrates[substrate_name].initial_value = 0.0
                self.substrates[substrate_name].current_value = 0.0
                self.substrates[substrate_name].active_time_ranges = None
                self.substrates[substrate_name].applied = False