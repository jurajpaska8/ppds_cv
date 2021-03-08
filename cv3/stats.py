import matplotlib.pyplot as plt


def plot(res: list):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = res[0]
    y = res[1]
    z = res[2]
    ax.set_xlabel("Number of readers")
    ax.set_ylabel("Average read time in ms")
    ax.set_zlabel("Number of writer accesses")
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    ax.view_init(azim=30)
    plt.show()


data = []
readers = []
times = []
writer_accesses = []

for r in range(1, 11):
    for _ in range(10):
        readers.append(r)

for _ in range(10):
    for t in range(1, 11):
        times.append(t * 10)

f = open("uloha5_data.txt", "r")
for x in f:
    writer_accesses.append(float(x.rstrip()))

data.append(readers)
data.append(times)
data.append(writer_accesses)
plot(data)

print("END")
