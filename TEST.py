import cProfile
import multiprocessing
import pstats


# Funkcja, która będzie wykonywana równolegle
def square(n):
    return n * n

def a():
    for i in range(10000):
        a = square(square(4))

cProfile.run("a()", "my_func_stats")

p = pstats.Stats("my_func_stats")
p.sort_stats("cumulative").print_stats()
