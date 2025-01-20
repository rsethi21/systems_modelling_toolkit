import pandas as pd
import numpy as np

class Substrate:
    def __init__(
        self, name: str, initial_value: float, 
        substrate_type: str, activation_rate: str = None, 
        deactivation_rate: str = None, total_amt: float = None,
        other_state: str = None, active_time_ranges: str = None
    ):
        self.name = name # identify of the substrate
        if total_amt != None and not pd.isna(active_time_ranges): # checking that the initial value set is less than total value set if any
            assert initial_value <= total_amt, "total amount should be greater than or equal to initial value if given"
        self.initial_value = initial_value # set initial value
        self.current_value = initial_value # set current value to initial value

        # setting type of substrate that will guide how its rates will be managed
        assert substrate_type.lower() in ["enzyme", "receptor", "stimulus", "other"], "Substrate types allowed: enzyme, receptor, stimulus, other"
        self.substrate_type = substrate_type.lower()

        # if type is stimulus there must be both a total amount and time range to apply that stimulus over
        if self.substrate_type == "stimulus":
            one = not pd.isna(active_time_ranges) and not pd.isna(total_amt)
            two = total_amt != None and active_time_ranges !=None
            assert one or two, "Stimulus requires a specified amount added and the time that the total should be added."

        # only either total amount or other state should be specified as they both essentially do the same thing, except that total should be used if other state not known
        one = not pd.isna(other_state) and not pd.isna(total_amt)
        two = total_amt != None and other_state !=None
        if one and two:
            print("Only use total amount if other state is not known. This is because the initial values for the forms will serve as a total.")
            exit()
        # set the rest of the values
        self.total_amt = total_amt
        self.other_state = other_state
        if active_time_ranges != None and np.nan != active_time_ranges:
            temp = active_time_ranges.split(",")
            temp = [float(temp[0]), float(temp[1])]
            active_time_ranges = temp
        self.active_time_ranges = active_time_ranges
        self.applied = False # way to check if a stimulus has been applied to determine when to switch to rate
        if activation_rate == np.nan or activation_rate == None:
            self.activation_rate = "zero"
        else:
            self.activation_rate = activation_rate
        if deactivation_rate == np.nan or deactivation_rate == None:
            self.deactivation_rate = "zero"
        else:
            self.deactivation_rate = deactivation_rate