from numba import cuda
import numpy
import math
from matplotlib import image
from matplotlib import pyplot


@cuda.jit
def my_kernel_2D(io_array):
    x, y = cuda.grid(2)
    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x, y] *= 2


@cuda.jit
def find_number(io_array, number):
    """
    Funkcia najde cislo number v poli a vypise na ktorej pozicii bolo najdene.
    :param io_array: Pole celych cisiel, moze byt nahodna permutacia
    :param number: hladane cislo
    :return: -
    """
    pos = cuda.grid(1)
    if pos < io_array.size:
        if io_array[pos] == number:
            print(f'Najdene na pozicii {pos}')
            io_array[pos] = -1


@cuda.jit
def change_pixels(io_array):
    """
    Funkcia zmeni hodnoty pixelov na 10 percent z povodnej hodnoty obrazku. Vysledkom je tmava verzia obrazku
    :param io_array: pole reprezentujuce pixely obrazku
    :return: -
    """
    x, y = cuda.grid(2)
    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x, y, 0] *= 0.1
        io_array[x, y, 1] *= 0.1
        io_array[x, y, 2] *= 0.1


# find number
data = numpy.random.permutation(2048)
threadsperblock = 128
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock
find_number[blockspergrid, threadsperblock](data, 60)
print(data)

# change pixels
data = image.imread('chrome2x-8bit.png')
# show image
pyplot.imshow(data)
pyplot.show()
threadsperblock = (32, 32)
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)
# compute pixels and show
change_pixels[blockspergrid, threadsperblock](data)
pyplot.imshow(data)
pyplot.show()

## cvicenie
# data = numpy.ones((16, 16))
# threadsperblock = (16, 16)
# blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
# blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
# blockspergrid = (blockspergrid_x, blockspergrid_y)
# my_kernel_2D[blockspergrid, threadsperblock](data)
# print(data)


