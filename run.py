#!/usr/bin/env python3.8
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from statistics import median
from textwrap import wrap


def index_by_substring(lst: list, func: str):
    for i, item in enumerate(lst):
        if func in item:
            return i


def get_median_for_func(time_dict: dict, func: str):
    acc = []
    for f, t in time_dict.items():
        if f == func:
            acc.append(t)
    return median(acc)


def plot_chart(scalar_medians: dict, auto_vec_medians: dict, intrinsic_medians: dict):
    num_func = len(auto_vec_medians)
    labels = ["scalar", "auto_vec", "Intrinsics"]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rect_list = []
    # This is a loop because we can have more than 2 funcs
    for i, func in enumerate(auto_vec_medians):
        x_position = (x - (0.5 * width) * (num_func - 1)) + i * width
        rect_list.append(ax.bar(x_position, [scalar_medians[func],
                                             auto_vec_medians[func], 
                                             intrinsic_medians[func]], 
                        width, label=func))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Runtime(s)")
    title = "Comparsion between ICX auto_vec and intrinsic (-mavx2)"
    ax.set_title("\n".join(wrap(title, 60)))
    ax.set_xticks(x, labels)
    ax.legend()

    for rect in rect_list:
        ax.bar_label(rect, padding=3)

    fig.tight_layout()
    plt.savefig("result.png")


if __name__ == "__main__":
    compiler = "clang"
    count = 15
    functions = ["s271", "s274"]
    scalar_times = {}
    auto_vec_times = {}  # key: func, value: time
    intrinsic_times = {}

    print("Running {} times".format(count))

    print("Running scalar")
    for i in range(count):
        result = subprocess.run(
            "./bin/{}/tsvc_scalar_relaxed".format(compiler), stdout=subprocess.PIPE)
        splited_lst = result.stdout.decode("utf-8").split()

        for func in functions:
            index_time = index_by_substring(splited_lst, func)
            t = float(splited_lst[index_time + 1])
            scalar_times[func] = t

    print("Running auto_vec")
    for i in range(count):
        result = subprocess.run(
            "./bin/{}/tsvc_auto_vec_relaxed".format(compiler), stdout=subprocess.PIPE)
        splited_lst = result.stdout.decode("utf-8").split()

        for func in functions:
            index_time = index_by_substring(splited_lst, func)
            t = float(splited_lst[index_time + 1])
            auto_vec_times[func] = t

    print("Running intrinics")
    for i in range(count):
        result = subprocess.run(
            "./bin/{}/tsvc_intrinsic_relaxed".format(compiler), stdout=subprocess.PIPE)
        splited_lst = result.stdout.decode("utf-8").split()

        for func in functions:
            index_time = index_by_substring(splited_lst, func)
            t = float(splited_lst[index_time + 1])
            intrinsic_times[func] = t

    # Get median runtime for all functions
    scalar_medians = {}
    auto_vec_medians = {}  # key: func, value: median
    intrinsic_medians = {}
    for func in functions:
        scalar_medians[func] = get_median_for_func(scalar_times, func)
    for func in functions:
        auto_vec_medians[func] = get_median_for_func(auto_vec_times, func)
    for func in functions:
        intrinsic_medians[func] = get_median_for_func(intrinsic_times, func)
    # Do Ploting
    plot_chart(scalar_medians, auto_vec_medians, intrinsic_medians)
