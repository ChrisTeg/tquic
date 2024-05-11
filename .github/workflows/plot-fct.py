#!/usr/bin/env python3

import os
import sys

import json
import matplotlib.pyplot as plt
import numpy as np

# QUIC implements
IMPLS = ["tquic", "gquiche", "lsquic", "picoquic", "quiche"]

# Different modes
MODES = ["1rtt", "0rtt"]

# Different loss rates
RATES = [0, 1, 3, 5]

# Running count for each test
COUNT = 30


# Read a measurement file generated by fct testing
def read_data(data_dir, impl, cc, mode, loss):
    dirname = "fct%s-%s-%s" % (mode, cc, impl)
    filename = "fct%s-%s-%s-%s.json" % (mode, loss, cc, impl)
    path = os.path.join(data_dir, dirname, filename)
    try:
        with open(path) as f:
            data = json.load(f)
            return data["measurements"][0][0]["data"]
    except:
        return None


# Plot the throughput graph for the specified CC algorithm under different file
# modes and packet loss rates.
def plot(data_dir, cc):
    fig, axs = plt.subplots(len(MODES), len(RATES), figsize=(15,10))
    x = np.linspace(0, COUNT, COUNT)
    for i in range(len(MODES)):
        for j in range(len(RATES)):
            for impl in IMPLS:
                data = read_data(data_dir, impl, cc, MODES[i], RATES[j])
                if data is None or len(data) != COUNT:
                    continue
                axs[i, j].plot(x, data, label=impl, marker=".")
                axs[i, j].set_xlabel("Run #")
                axs[i, j].set_ylabel("FCT")
                axs[i, j].set_title("%s loss rate %s%%" % (MODES[i], RATES[j]))
                axs[i, j].legend()
    plt.suptitle(cc.upper())
    plt.tight_layout()
    plt.savefig("fct-%s.png" % (cc), dpi=300)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s [data_dir]" % (sys.argv[0]))
        exit(1)

    data_dir= sys.argv[1]
    plot(data_dir, "bbr")
    plot(data_dir, "cubic")

