import matplotlib.pyplot as plt


def time_plotter(file):
    """
    Takes a input file and extracts cores and time, separated by ":"
    Creates a timings.png containing the values.
    """
    
    threads_timings = []

    with open(file) as f:
        for line in f:
            if line[0].isdigit():
                threads_timings.append(line.strip().split(":"))
    
    timing = [i[0] for i in threads_timings]
    threads = [i[1] for i in threads_timings]

    plt.scatter(timing, threads)
    plt.title("Timings per number of threads")
    plt.savefig('output/timings.png')

if __name__ == "__main__":
    time_plotter('output/timings.txt')