import argparse
import pandas as pd
import json

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--original", help="original rates csv", required=True)
parser.add_argument("-a", "--adapter", help="new rates json", required=True)
parser.add_argument("-f", "--fitted", help="path to csv file for fitted rates", required=True)
if __name__ == "__main__":
    args = parser.parse_args()
    adapter = json.load(open(args.adapter))
    df = pd.read_csv(args.original, index_col=0)
    for i, row in df.iterrows():
        if df.loc[i,"name"] in adapter.keys():
            df.loc[i, "value"] = adapter[df.loc[i,"name"]]
    df.to_csv(args.fitted, index=True)