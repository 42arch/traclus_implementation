import math
from argparse import ArgumentError
from .distance_functions import angular_distance, perpendicular_distance

DECIMAL_MAX_DIFF_FOR_EQUALITY = 0.0000001

_delta = 0.000000001


def set_max_delta_for_equality(delta):
    _delta = delta


# 向量类
class Vector(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        if x != 0.0:
            self.angle = math.degrees(math.atan(float(y) / x))
        elif y == 0.0:
            self.angle = 0
        elif y > 0.0:
            self.angle = 90
        elif y < 0.0:
            self.angle = -90

        if self.x < 0:
            self.angle += 180

    # 两个向量的点积方法
    def dot_product_with(self, other_vector):
        return self.x * other_vector.x + self.y * other_vector.y

    # 字典格式
    def as_dict(self):
        return {'x': self.x, 'y': self.y}

    # 被矩阵相乘
    def multipled_by_matrix(self, x1, y1, x2, y2):
        new_x = self.x * x1 + self.y * x2
        new_y = self.x * y1 + self.y * y2
        return Vector(new_x, new_y)

    # 旋转
    def rotated(self, angle_in_degrees):
        cos_angle = math.cos(math.radians(angle_in_degrees))
        sin_angle = math.sin(math.radians(angle_in_degrees))
        return self.multipled_by_matrix(x1=cos_angle, y1=sin_angle, x2=-sin_angle, y2=cos_angle)

    # 判断相等
    def almost_equals(self, other):
        return abs(self.x - other.x) <= DECIMAL_MAX_DIFF_FOR_EQUALITY and abs(
            self.y - other.y) <= DECIMAL_MAX_DIFF_FOR_EQUALITY

    def __eq__(self, other):
        return other is not None and abs(self.x - other.x) < _delta and abs(self.y - other.y) < _delta

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "x: " + str(self.x) + "| y:" + str(self.y)


def distance(diff_x, diff_y):
    return math.sqrt(diff_x * diff_x + diff_y * diff_y)


# 点类
class Point(Vector):
    def __init__(self, x, y):
        Vector.__init__(self, x, y)

    # 两点间距离
    def distance_to(self, other_point):
        diff_x = other_point.x - self.x
        diff_y = other_point.y - self.y
        return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))

    # # 两点间（经纬度）地理距离（米）
    # def geo_distance_to(self, other_point):
    #     pass

    def distance_to_projection_on(self, line_segment):
        diff_x = self.x - line_segment.start.x
        diff_y = self.y - line_segment.start.y

        return abs(diff_x * line_segment.unit_vector.y - diff_y * line_segment.unit_vector.x)

    def rotated(self, angle_in_degrees):
        result = Vector.rotated(self, angle_in_degrees)
        return Point(result.x, result.y)


class LineSegment:
    """ 线段类 包含两个点 """
    @staticmethod
    def from_tuples(start, end):
        return LineSegment(Point(start[0], start[1]), Point(end[0], end[1]))

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = start.distance_to(end)

        if self.length > 0.0:
            unit_x = (end.x - start.x) / self.length
            unit_y = (end.y - start.y) / self.length
            self.unit_vector = Point(unit_x, unit_y)  # 单位向量

    def as_dict(self):
        return {'start': self.start.as_dict(), 'end': self.end.as_dict()}

    # 与另一条线段的正弦角度
    def sine_of_angle_with(self, other_line_segment):
        return self.unit_vector.x * other_line_segment.unit_vector.y - self.unit_vector.y * other_line_segment.unit_vector.x

    # 从线段开始点到另一点投影的距离
    def dist_from_start_to_projection_of(self, point):
        diff_x = self.start.x - point.x
        diff_y = self.start.y - point.y
        return abs(diff_x * self.unit_vector.x + diff_y * self.unit_vector.y)

    # 从线段尾点到一个点投影点的距离
    def dist_from_end_to_projection_of(self, point):
        diff_x = self.end.x - point.x
        diff_y = self.end.y - point.y
        return abs(diff_x * self.unit_vector.x + diff_y * self.unit_vector.y)

    def almost_equals(self, other):
        return self.start.almost_equals(other.start) and self.end.almost_equals(other.end)

    def __eq__(self, other):
        return other is not None and (self.start == other.start and self.end == other.end)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "start: " + str(self.start) + " --- end: " + str(self.end)


class Trajectory:
    """ 轨迹类 ， 包含多个点集"""
    def __init__(self, id):
        self.points = []
        self.id = id

    #  检查指标参数
    def check_indice_args(self, start, end):
        if start < 0 or start > len(self.points) - 2:
            raise ArgumentError('invalid start index')
        elif end <= start or end > len(self.points) - 1:
            raise ArgumentError('invalid end index')

    def model_cost(self, start, end):
        self.check_indice_args(start, end)
        return math.log(self.points[start].distance_to(self.points[end]), 2)

    def encoding_cost(self, start, end):
        self.check_indice_args(start, end)
        approximation_line = LineSegment(self.points[start], self.points[end])

        total_perp = 0.0
        total_angular = 0.0
        for i in range(start, end):
            line_seg = LineSegment(self.points[i], self.points[i + 1])
            total_perp += perpendicular_distance(approximation_line, line_seg)
            total_angular += angular_distance(approximation_line, line_seg)

        if total_perp < 1.0:
            total_perp = 1.0
        if total_angular < 1.0:
            total_angular = 1.0

        return math.log(total_perp, 2) + math.log(total_angular, 2)

    def get_partition(self):
        return range(0, len(self.points))

    def __repr__(self):
        return str(self.points)
