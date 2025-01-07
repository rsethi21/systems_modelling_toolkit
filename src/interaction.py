class Interaction:
    def __init__(
        self, name: str, resultant: str, stimulus: str, rate: str, effect: [1, -1], Kd: str = None, n: str = None
    ):
        self.name = name
        self.resultant = resultant # substrate affected
        self.stimulus = stimulus # substrate causing the effect
        self.rate = rate # absolute value rate of the effect
        self.effect = effect # sign of the rate
        self.Kd = Kd
        self.n = n
    
    def calculate_contribution(self, substrates, rates):
        if self.Kd != None and self.n != None: # if the goodwin oscillator terms are not none
            if self.effect > 0: # if effect if positive
                return (substrates[self.stimulus].current_value)**rates[self.n].current_value / ((substrates[self.stimulus].current_value)**rates[self.n].current_value + rates[self.Kd].current_value**rates[self.n].current_value) # appropriate positive feedback
            else:
                return rates[self.Kd].current_value**rates[self.n].current_value / ((substrates[self.stimulus].current_value)**rates[self.n].current_value + rates[self.Kd].current_value**rates[self.n].current_value) # appropriate negative feedback
        else:
            return substrates[self.stimulus].current_value # just the substrate affecting

    @classmethod
    def calculate_base_contributions(cls, resultant, substrates):
        if resultant.other_state != None: # if there is an other state
            return substrates[resultant.other_state].current_value, resultant.current_value # return other state and current value for positive and negative values
        elif resultant.total_amt != None:
            return resultant.total_amt - resultant.current_value, resultant.current_value # if total amount not none then convert to not and current
        else:
            return 1, resultant.current_value # if neither available then l ikely a non-enzyme so no drive rate

    @classmethod
    def represent_base_contribution(cls, resultant):
        if resultant.other_state != None: # if there is an other state
            return resultant.other_state, resultant.name # return other state and current value for positive and negative values
        elif resultant.total_amt != None:
            if resultant.substrate_type != "stimulus":
                return f"total - {resultant.name}", resultant.name # if total amount not none then convert to not and current
            else:
                return "", resultant.name # if total amount not none then convert to not and current
        else:
            return "", resultant.name # if neither available then likely a stimulus so no drive rate


    def represent_contribution(self, stimulus, rates):
        if self.Kd != None and self.n != None: # if the goodwin oscillator terms are not none
            if self.effect > 0: # if effect if positive
                return f"{stimulus.name}^{rates[self.n].name} / ({stimulus.name}^{rates[self.n].name} + {rates[self.Kd].name}^{rates[self.n].name})" # appropriate positive feedback
            else:
                return f"{rates[self.Kd].name}^{rates[self.n].name} / ({stimulus.name}^{rates[self.n].name} + {rates[self.Kd].name}^{rates[self.n].name})" # appropriate negative feedback
        else:
            return stimulus.name # just the substrate affecting