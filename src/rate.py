class Rate:
    def __init__(
        self, name: str, value: float, upper_bound = 0.0, lower_bound = 1.0, bound_type: ["int", "real"] = "real", fixed: bool = False
    ):
        self.name = name # rate identity
        self.initial_value = value # intial value of the rate
        self.current_value = value # current value of the rate
        self.fixed = fixed # fixed depending on whether this rate will be fitted
        # bounds/types for the fitting process
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.bound_type = bound_type