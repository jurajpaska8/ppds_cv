from time import perf_counter

from numba import cuda
import math
from matplotlib import image
from matplotlib import pyplot
import numpy as np


@cuda.jit
def change_pixels(io_array):
    """
    Funkcia zmeni hodnoty pixelov na 10 percent z povodnej hodnoty obrazku. Vysledkom je tmava verzia obrazku
    :param io_array: pole reprezentujuce pixely obrazku
    :return: -
    """
    x = cuda.grid(1)
    if x < io_array.size:
        io_array[x, 0] *= 0.1
        io_array[x, 1] *= 0.1
        io_array[x, 2] *= 0.1


# change pixels
data = image.imread('chrome2x-8bit.png')
# show image
pyplot.imshow(data)
pyplot.show()
# threadsperblock = (32, 32)
# blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
# blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
# blockspergrid = (blockspergrid_x, blockspergrid_y)

# compute pixels and show
data_gpu = []
gpu_out = []
streams = []

for _ in range(64):
    streams.append(cuda.stream())

t_start = perf_counter()

for k in range(64):
    data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

for k in range(64):
    change_pixels[1, 64, streams[k]](data_gpu[k])

for k in range(64):
    gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

t_end = perf_counter()
print(f'Total time: {t_end - t_start:.2f} s')

pyplot.imshow(gpu_out)
pyplot.show()