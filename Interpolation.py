from Point import Point
import time


class Interpolation:
    iteration_count = 0
    __serializable = False
    __points = []
    __intervals = []
    __has_temporary_point = False
    __interpolation_point_x = 0
    __width = 4
    __iterations = 0

    def __init__(self, points=[], method=None, serializable=False):
        self.__serializable = serializable
        self.__points = points
        self.lagrangian = []
        self.__aitken_table = []
        self.__method = method

    def count(self, point, filename):
        pass

    def get_interval(self, point):
        pass

    def get_points(self):
        return list(self.__points)

    def get_split_points(self):
        xs = [x.get_x() for x in self.__points]
        ys = [x.get_y() for x in self.__points]
        return (xs, ys)

    def get_interpolation_point_x(self):
        return self.__interpolation_point_x

    def set_interpolation_point_x(self, x):
        self.__interpolation_point_x = x

    def get_width(self):
        return self.__width

    def set_width(self, width):
        self.__width = width

    def get_table(self):
        if self.__aitken_table:
            return self.__aitken_table
        else:
            return None

    def set_table(self, table):
        self.__aitken_table = table

    def __len__(self):
        return len(self.get_points())

    def add_point(self, point):
        if not isinstance(point, Point):
            print("Not a valid point")
        else:
            self.__points.append(point)
            self.__points.sort(key=lambda x: x.get_x())

    def add_temporary_point(self):
        pass

    def remove_point(self, point_index):
        pass

    def remove_temporary_point(self):
        pass

    def clear_points(self):
        self.__points = []
        self.__interpolation_point_x = None

    def serialize(self):
        return False

    def deserialize(self):
        return False

    def write_result_to_file(self, filename, point, interval):
        pass

    def is_in_interval(self, x):
        less = x <= max(self.get_points(), key=lambda x: x.get_x()).get_x()
        more = x >= min(self.get_points(), key=lambda x: x.get_x()).get_x()
        return less and more

    def method(self, x, points, data):
        if len(data) == 1:
            return data[0]
        else:
            A = self.method(x, points[1:], data[1:]) * \
                (x - points[0])/(points[-1] - points[0])
            B = self.method(x, points[:-1], data[:-1]) * \
                (x - points[-1])/(points[0] - points[-1])
            return A + B

    def recursive_Lagrangian(self, i, j):
        x0 = self.get_points()[i].get_x()
        y0 = self.get_points()[i].get_y()
        x1 = self.get_points()[j].get_x()
        y1 = self.get_points()[j].get_y()
        x = self.get_interpolation_point_x()
        if (x0 - x1) == 0 or (x1 - x0) == 0:
            return y0
        elif i + 1 == j:
            left = ((x - x1) / (x0 - x1)) * y0
            right = ((x - x0) / (x1 - x0)) * y1
            return left + right
        else:
            p_i_k_1 = self.recursive_Lagrangian(i, j - 1)
            p_i_1_k = self.recursive_Lagrangian(i + 1, j)
            left = ((x - x1) / (x0 - x1)) * p_i_k_1
            right = ((x - x0) / (x1 - x0)) * p_i_1_k
            return left + right

    def Lagrangian_method(self):
        x = self.get_interpolation_point_x()
        for basis in self.get_points():
            if basis.get_x() == x:
                # print("Lagrangian iterations: ", 0)
                return basis.get_y()
        numerator = 1
        denominator = 1
        addendum = 0
        addendums = []
        iterations = 0
        for j in range(len(self)):
            x_in_i = self.get_points()[j].get_x()
            for i in range(len(self)):
                if i != j:
                    iterations += 1

                    numerator *= (x - self.get_points()[i].get_x())
            for i in range(len(self)):
                if i != j:
                    iterations += 1

                    denominator *= (x_in_i - self.get_points()[i].get_x())
            # print("numerator: {} denominator: {}".format(numerator, denominator))
            if denominator != 0:
                addendum = (numerator/denominator) * \
                    self.get_points()[j].get_y()
            else:
                addendum = numerator * self.get_points()[j].get_y()
            addendums.append(addendum)
            addendum = 0
            numerator = 1
            denominator = 1
        result = sum(addendums)
        # print("Lagrangian iterations: ", iterations)
        # print(addendums)
        # print("(132) Lagrangian_method result: ", result)
        return result

    def build_Lagrangian(self):
        current_string = ""
        for j in range(len(self)):
            x_in_i = self.get_points()[j].get_x()
            for i in range(len(self)):
                if i != j:
                    current_string += "(x - %.2f)" % self.get_points()[
                        i].get_x()
            current_string += "\n" + "_" * \
                (len(self)*11) + "*%.2f \n" % self.get_points()[j].get_y()
            for i in range(len(self)):
                if i != j:
                    current_string += "(%.2f - %.2f)" % (x_in_i,
                                                         self.get_points()[i].get_x())
            self.lagrangian.append(current_string)
            current_string = ""

    def find_Aitken_row_for_x(self, x):
        if not self.is_in_interval(x):
            print("ValueError")
            return -1
        point_idx = 0
        while self.get_points()[point_idx].get_x() < x:
            point_idx += 1
        return point_idx - 1

    def init_Aitken(self):
        table = []
        points_length = len(self)
        for i in range(points_length):
            row = []
            row.append(i)
            row.append(self.get_points()[i].get_x())
            row.append(self.get_points()[i].get_y())
            row.extend([None] * self.get_width())
            table.append(row)
        return table

    def build_Aitken(self, lookup_row):
        points_length = len(self)
        x = self.get_interpolation_point_x()
        points = self.get_points()
        width = self.get_width()
        Aitken_table = self.init_Aitken()
        # min so we don't get outside the points we have vertically
        for i in range(lookup_row, min(lookup_row + width, points_length-1)):
            p_i = points[i]
            # min so we don't get outside the points we have horizontally
            for k in range(1, min(width + 1, points_length - i)):
                self.__iterations += 1
                res = self.recursive_Lagrangian(i, i + k)
                # 3 - margin from i & points in first 3 columns
                Aitken_table[i][k - 1 + 3] = round(res, 3)
            width -= 1
    #             print("px: %.1f, py: %.2f, i: %d, j: %d, y: %f"%(p_i[0],p_i[1], i,j,res))
        self.set_table(Aitken_table)
        return Aitken_table

    def find_delta(self, a, b, round_to=4):
        return round(abs(b - a), round_to)

    def find_y(self, table, lookup_row_idx):
        j = 3
        deltas = []
        deltas_row = list(table[lookup_row_idx])
        if deltas_row[j] == None:
            return 0
        while j+1 < len(deltas_row) and deltas_row[j + 1] != None:
            self.__iterations += 1
            delta = self.find_delta(deltas_row[j+1], deltas_row[j])
            deltas.append(delta)
            j += 1
        idx = 0
        while idx + 1 < len(deltas) and deltas[idx + 1] <= deltas[idx]:
            idx += 1
        result = deltas_row[3 + idx + 1]
        if result == None:
            result = deltas_row[deltas_row.index(None) - 1]
        print("List of deltas for a series %d: " %
              lookup_row_idx, deltas, "\n")
        return result

    def test(self):
        x = self.get_interpolation_point_x()
        if not(self.is_in_interval(x)):
            print("x = %f is outside the array of points." % x, "\n")
            return False
        start_Aitken = time.time()
        y1 = self.Lagrangian_method()
        print("Lagrangian result: for the entered \ty(%.4f) = %.6f" % (x, y1))
        lookup_row = self.find_Aitken_row_for_x(x)
        table = self.build_Aitken(lookup_row)

        xs, ys = self.get_split_points()
        # aaa = self.method(x, xs, ys)
        # print("Aitken table for x =", x, "\n")
        # for print_row in table:
        #     print("\t", print_row)
        # print("-"*30, "\n")
        y = self.find_y(table, lookup_row)
        end_Aitken = time.time()
        # print("Aitken iterations: ", self.__iterations)
        self.__iterations = 0
        # print("Aitken time: ", end_Aitken - start_Aitken)
        self.build_Lagrangian()
        print("Aitken result: for the entered \ty(%.4f) = %.4f" % (x, y))
        start_Lagrangian = time.time()
        end_Lagrangian = time.time()
        # print("Lagrangian time: ", end_Lagrangian - start_Lagrangian)
        print()
        return y
