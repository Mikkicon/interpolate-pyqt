class Point:
    __x = 0.0
    __y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y):
        self.__y = y

    def __str__(self):
        return "(%.4f, %.4f)" % (self.get_x(), self.get_y())

    def __repr__(self):
        return "(%.4f, %.4f)" % (self.get_x(), self.get_y())

    def __iter__(self):
        return iter((__x, __y))
