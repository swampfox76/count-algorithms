import sys
import operator
from memory_profiler import profile
import pandas as pd
import numpy as np

from count_median_sketch import count_median_sketch, check_median
from count_min_sketch import count_min_sketch, check_min
from count_sketch import count_sketch

def linear_count(data, bin_number, bin_size):
    counts = {}
    for d in data:
        if d in counts:
            counts[d] += 1
        else:
            counts[d] = 1
    return dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True)[:bin_size])

def error(observed, query_func, bin_size, truth, n=1):
    vec = []
    for k in truth.keys():
        vec.append(truth[k] - query_func(observed, k, bin_size))
    return np.linalg.norm(vec, n)

@profile
def run(algorithm, file_name, bin_number, bin_size):
    df = pd.read_csv(file_name, index_col='Id')
    data = []
    for row in df.iterrows():
        data.extend(row[1]['Name'] * row[1]['Count'])
    return eval(algorithm)(data, bin_number, bin_size)

if __name__ == '__main__':
    if len(sys.argv) is 5:
        algorithm = sys.argv[1]
        file_name = sys.argv[2]
        bin_number = int(sys.argv[3])
        bin_size = int(sys.argv[4])
        bins = run(algorithm, file_name, bin_number, bin_size)
        bins2 = run('linear_count', file_name, bin_number, bin_size)
        print bins
        print error(bins, check_min, bin_size, bins2)
    else:
        print "python check_memory_usage.py algorithm file_name bin_number bin_size"
        sys.exit()