"""
Takes a input file created by assignment3.sh and extracts values
for cores and time and plots them.
output: timings.png
"""
import matplotlib.pyplot as plt


def time_plotter(file):
    """
    Takes a input file and extracts cores and time, separated by ":"
    Creates a timings.png containing the values.
    """

    # creates list to hold threads and timings
    threads_timings = []

    # opens file and extracts values
    with open(file, 'r', encoding="utf8") as f_vals:
        for line in f_vals:
            if line[0].isdigit():
                threads_timings.append(line.strip().split(":"))

    # separate values through list comprehension
    timing = [i[0] for i in threads_timings]
    threads = [i[1] for i in threads_timings]

    # plot values and save to file
    plt.scatter(timing, threads)
    plt.title("Timings per number of threads")
    plt.savefig('output/timings.png')

if __name__ == "__main__":
    time_plotter('output/timings.txt')
