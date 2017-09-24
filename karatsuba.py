import math
import argparse
import timeit


def num_length(num):
    digits = 0
    if num > 0:
        digits = int(math.log10(num)) + 1
    elif num == 0:
        digits = 1
    elif num < 0:
        digits = int(math.log10(-num)) + 1  # +2 if count '-'
    return digits


def num_to_list(a):
    return list(map(str, str(a)))


def split(a, m):
    a_list = num_to_list(a)
    a0, a1 = a_list[0:m], a_list[m:]
    return int(''.join(a0)), int(''.join(a1))


def karatsuba(x, y, base=10):
    # Recursion base case
    if num_length(x) or num_length(y) < 10:
        return x*y
    # find m~=n/2
    m = max(x, y)/2
    # split numbers
    x0, x1 = split(x, m)
    y0, y1 = split(y, m)
    # calculate z0, z1, z2
    z0 = karatsuba(x1, y1)
    z2 = karatsuba(x0, y0)
    z1 = karatsuba((y1+y0), (x0+x1))
    # return final result
    return z2*base**(2*m) + (z1-z0-z2)*base**m+z0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multiplication using Karatsuba algorithm")
    parser.add_argument("-x", type=int,
                        help="Specify first number", required=True)
    parser.add_argument("-y", type=int,
                        help="Specify second number", required=True)
    args = parser.parse_args()
    x, y = args.x, args.y
    start_time = timeit.default_timer()
    print(karatsuba(x, y))
    print("Karatsuba multiplication Used: ", timeit.default_timer() - start_time)
    start_time = timeit.default_timer()
    print(x*y)
    print("Python internal multiplication Used: ", timeit.default_timer() - start_time)





