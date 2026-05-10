import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import os

folder = "/home/rsethi/school_rsh/PKH/systems_modelling_toolkit/data/outputs/albert"
paths = [os.path.join(folder, f) for f in os.listdir(folder) if ".csv" in f]
exp = "atp"
time = "time"
value = "pAKT"
factor = 4000/4000
start = 2919
end = 4000
times = [int(start*factor), int(end*factor)]

for path in paths:
    df_ori = pd.read_csv(path)
    df = df_ori.loc[times[0]:times[1], value]
    df = pd.DataFrame.from_dict({time: list(range(len(df.index))), value: list(df)})

    x = np.array(df[time])
    y = np.array(df[value])
    iv=y[0]
    def exponential(x, a, b):
        return iv * a**(b*x)
    params, covar = curve_fit(exponential, x, y)
    print(path)
    print(params)
    print(1 - (params[0]**params[1]))
    print(max(y))
    print("-----------------------------")

import matplotlib.pyplot as plt
import numpy as np

# Data
conditions = ["LPS", "ATP", "ATP + Ca²⁺", "ATP + EGTA"]
increase = [0.0025, 0.0018, 0.0020, 0.0016]
decay = [-0.00036, -0.0240, -0.0294, -0.0196]

# Bar settings
x = np.arange(len(conditions))
width = 0.35

# Create plot
fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width/2, increase, width, label="Increase", color="#4CAF50")
bars2 = ax.bar(x + width/2, decay, width, label="Decay", color="#F44336")

# Labels and styling
ax.set_ylabel("Value")
ax.set_title("Increase and Decay by Condition")
ax.set_xticks(x)
ax.set_xticklabels(conditions)
ax.legend()
ax.axhline(0, color="black", linewidth=0.8)

# Display values on bars
for bars in [bars1, bars2]:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (0.0005 if yval > 0 else -0.001), f"{yval:.4f}", ha="center", va="bottom" if yval > 0 else "top", fontsize=8)

fig.savefig("example.png")