import matplotlib.pyplot as plt

def cpu_percent_graph(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Time (sec)"], df["CPU Percentage"])
    plt.plot(df["Time (sec)"], df["CPU Percentage"])
    plt.xlabel("Time (sec)")
    plt.ylabel("CPU Percentage")
    plt.title("CPU Percentage vs Time")
    plt.show()

def memory_percent_graph(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Time (sec)"], df["Memory Percentage"])
    plt.plot(df["Time (sec)"], df["Memory Percentage"])
    plt.xlabel("Time (sec)")
    plt.ylabel("Memory Percentage")
    plt.title("Memory Percentage vs Time")
    plt.show()

def disk_percent_graph(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Time (sec)"], df["Disk Percentage"])
    plt.plot(df["Time (sec)"], df["Disk Percentage"])
    plt.xlabel("Time (sec)")
    plt.ylabel("Disk Percentage")
    plt.title("Disk Percentage vs Time")
    plt.show()