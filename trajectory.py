import math

from distance_functions import perpendicular_distance, angular_distance
from geometry import LineSegment, Point
from argparse import ArgumentError


# 轨迹类
class Trajectory:
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