import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import pdb
import json

time_set = 5099

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", help="folder with tracks and output", required=True)
parser.add_argument("-c", "--column", help="column title to plot", required=True)
parser.add_argument("-r", "--resolution", help="resolution of simulation", required=False, type=int, default=10000)
parser.add_argument("-m", "--maxtime", help="max time of simulation", required=False, type=int, default=time_set+1)
parser.add_argument("-s", "--start", help="start time of plotting", required=True, type=int)
parser.add_argument("-e", "--end", help="start time of plotting", required=True, type=int)
parser.add_argument("-d", "--deduct", help="time of release", required=True, type=int)
parser.add_argument("-p", "--points", help="plot experimental plots", required=False, default=None)

if __name__ == "__main__":
    args = parser.parse_args()
    series = {}
    series_unnormalized = {}
    factor = float(args.resolution/args.maxtime)
    start = args.start*factor
    end = args.end*factor
    release = (args.deduct-args.start)*factor
    times = []
    for file in os.listdir(args.folder):
        if "csv" in file:
            path = os.path.join(args.folder, file)
            df = pd.read_csv(path)
            values = np.array(df.loc[start:end, args.column])
            values = (values - min(values))/(max(values) - min(values))
            series[file[0:file.index(".csv")]] = values
            series_unnormalized[file[0:file.index(".csv")]] = np.array(df.loc[start:end, args.column])
    series["control"] = [0.0 for __ in range(len(series[list(series.keys())[0]]))]
    plotting_df = pd.DataFrame.from_dict(series)
    plotting_df.plot.line()
    plt.axvline(x=release, color='black', linestyle='--', label='Stimuli Washed')
    plt.xlabel('Time (min)')
    plt.ylabel('pAKT')
    plt.grid(True)
    plt.legend(title='Condition', loc="upper right", fontsize="xx-small")
    plt.savefig(os.path.join(args.folder, "experiment.png"))


    series_unnormalized["control"] = [1.0 for __ in range(len(series[list(series.keys())[0]]))]
    plotting_df_unnormalized = pd.DataFrame.from_dict(series_unnormalized)
    plotting_df_unnormalized.plot.line()
    try:
        all_points = json.load(open(args.points))
        for p in all_points:
            plt.plot(factor*(p[0]-args.start), p[1], ".", color=p[2], markersize=10)
    except:
        pass
    plt.axvline(x=release, color='black', linestyle='--', label='Stimuli Washed')
    plt.xlabel('Time (min)')
    plt.ylabel('pAKT')
    plt.grid(True)
    plt.legend(title='Condition', loc="upper right", fontsize="xx-small")
    plt.savefig(os.path.join(args.folder, "experiment_unnormalized.png"))