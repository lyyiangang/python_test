
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file', type = str, default = '')
args = parser.parse_args()
import pickle
with open(args.file, 'rb') as fid:
    data = pickle.load(fid)
print(data)