# from AitkenInterpolation import test
from Interpolation import Interpolation
from Point import Point
from random import random, sample
import numpy as np


def user(interpolation_ins):

    points = []
    print("And now you can enter your base points on which the interpolation will take place, in the format: \n\\tx1 y1 \n \tx2 y2 \n")
    """
    0.0 1.0
    0.2 1.02
    0.4 1.08
    0.6 1.12
    0.8 1.34
    1.0 1.54
    1.2 1.81
    1.4 2.15

    """
    user_input = input(
        "Type points with [x] and [y] with a space and Enter after each point \ n When done - press Enter again\n...")
    interpolation_ins.clear_points()
    while user_input:
        x, y = [float(x) for x in user_input.strip().split()]
        point = Point(x, y)
        interpolation_ins.add_point(point)
        print("Point ", point, " added")
        print("Array: ", interpolation_ins.get_points(), "\n")
        user_input = input("...")
    points.sort(key=lambda x: x.get_x())
    x = input("Now enter x for interpolation...")
    while x:
        x = float(x)
        interpolation_ins.set_interpolation_point_x(x)
        interpolation_ins.test()
        x = input("More values for x...")


def generate_points(amount):
    points = []
    for i in range(amount):
        x = (random() * i) + i
        y = (random() * i) + 2 * i
        points.append(Point(x, y))
    # print(points)
    return points


def profiling(test_runs):
    interpolation_ins = Interpolation()
    for run in range(1, test_runs + 1):
        amount = 2**run
        points = generate_points(amount)
        interpolation_points = [p.get_x() + (random() - 0.5)
                                for p in sample(points, int(len(points) * 0.5))]
        for p in points:
            interpolation_ins.add_point(p)
        print("Points length is ", amount)
        for x in interpolation_points:
            interpolation_ins.set_interpolation_point_x(x)
            y = interpolation_ins.test()
        interpolation_ins.clear_points()


def compare_small(points):
    interpolation_ins = Interpolation()
    interpolation_ins.set_width(20)

    for (x, y) in points:
        p = Point(x, y)
        interpolation_ins.add_point(p)
    xs = np.arange(min(points, key=lambda x: x[0])[0], max(
        points, key=lambda x: x[0])[0], 0.05)
    ys_L = []
    ys_E = []
    for x in xs:
        interpolation_ins.set_interpolation_point_x(x)
        y_L = interpolation_ins.Lagrangian_method()
        y_E = interpolation_ins.test()
        ys_L.append(y_L)
        ys_E.append(y_E)
    print("Results\n", ys_L, "\n\n\n", ys_E)


def main():
    # test_xs = [0.1, 0.25, 0.3, 0.0, 2.4]
    test_xs = [1.4, 1.5]
    # points = [(0.0, 1.0), (0.2, 1.02), (0.4, 1.08), (0.6, 1.12),
    #           (0.8, 1.34), (1.0, 1.54), (1.2, 1.81), (1.4, 2.15)]
    points = [(0.0, 4.0), (0.5, 3.7), (1.4, 4.5757), (2.25, 4.333),
              (3.5, 4.167)]

    # print("To begin, the program will display 5 test runs for: ")
    # interpolation_ins = Interpolation()
    # interpolation_ins.set_width(6)
    # for (x, y) in points:
    #     p = Point(x, y)
    #     interpolation_ins.add_point(p)

    # for x in test_xs:
    #     print("x =", x)

    # for x in test_xs:
    #     interpolation_ins.set_interpolation_point_x(x)
    #     y = interpolation_ins.test()

    # user(interpolation_ins)
    compare_small(points)


if __name__ == '__main__':
    main()
    # testov = int(input("How many tests do you need to perform?"))
    # profiling(testov)
