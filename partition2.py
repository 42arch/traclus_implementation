# 轨迹分段
# 采用MDL原则把，通过垂直距离与角度距离定义MDL(par)和MDL(no_par), 如果MDL(par)大于MDL(no_par)，则在当前点的
# 前一个点进行切分

import math
from distance_functions import angular_distance, perpendicular_distance
from geometry import LineSegment

DISTANCE_OFFSET = 0.0000000001


def call_partition_trajectory(trajectory_point_list):
    """ 轨迹分段
    与下不同，输入为点列表
    :param trajectory_point_list: 轨迹线 点 列表
    :return:
    """
    if len(trajectory_point_list) < 2:
        raise ValueError

    # def encoding_cost_func(trajectory_line_segs, low, high, partition_line):
    #     return encoding_cost(trajectory_line_segs, low, high,
    #                          partition_line=partition_line,
    #                          angular_dist_func=angular_distance,
    #                          perpendicular_dist_func=perpendicular_distance)
    #
    # def partition_cost_func(trajectory_line_segs, low, high):
    #     return partition_cost(trajectory_line_segs, low, high,
    #                           model_cost_func=model_cost,
    #                           encoding_cost_func=encoding_cost)

    trajectory_line_segs = list(map(lambda i: LineSegment(trajectory_point_list[i], trajectory_point_list[i + 1]),
                                    range(0, len(trajectory_point_list) - 1)))
    return partition_trajectory(trajectory_line_segs=trajectory_line_segs)


def partition_trajectory(trajectory_line_segs):
    """轨迹分段
    切分依据：比较 MDL_par 和 MDL_no_par 的大小，如果 MDL_par 大于MDL_no_par 则在前一节进行切分
    :param trajectory_line_segs: 轨迹线线段列表
    :param partition_cost_func: MDL_par
    :param no_partition_cost_func: MDL_no_par
    :return: 切分点列表
    """
    if len(trajectory_line_segs) < 1:
        raise ValueError
    low = 0
    partition_points = [0]
    last_pt = trajectory_line_segs[len(trajectory_line_segs) - 1].end
    trajectory_line_segs.append(LineSegment(last_pt, last_pt))

    for high in range(2, len(trajectory_line_segs)):
        mdl_par = partition_cost(trajectory_line_segs, low, high)
        mdl_no_par = no_partition_cost(trajectory_line_segs, low, high)

        if trajectory_line_segs[high - 2].unit_vector.almost_equals(trajectory_line_segs[high - 1].unit_vector):
            continue
        # elif trajectory_line_segs[high].start.almost_equals(trajectory_line_segs[low].start) or \
        #         partition_cost_func(trajectory_line_segs, low, high) > \
        #         no_partition_cost_func(trajectory_line_segs, low, high):
        elif trajectory_line_segs[high].start.almost_equals(trajectory_line_segs[low].start) or mdl_par > mdl_no_par:
            partition_points.append(high - 1)
            low = high - 1

    partition_points.append(len(trajectory_line_segs) - 1)
    return partition_points


def partition_cost(trajectory_line_segs, low, high):
    """   MDL_par   轨迹分段开销
    MDL(cost) = L(H) + L(D|H)
    :param trajectory_line_segs:
    :param low:
    :param high:
    :param model_cost_func:
    :param encoding_cost_func:
    :return:
    """
    if low >= high:
        raise IndexError
    partition_line = LineSegment(trajectory_line_segs[low].start, trajectory_line_segs[high].start)

    model_cost = model_cost_func(partition_line)
    encoding_cost = encoding_cost_func(trajectory_line_segs, low, high, partition_line)
    # model_cost = model_cost_func(partition_line)
    # encoding_cost = encoding_cost_func(trajectory_line_segs, low, high, partition_line)
    return model_cost + encoding_cost


def no_partition_cost(trajectory_line_segs, low, high):
    """  计算MDL_no_par
    :param trajectory_line_segs:
    :param low:
    :param high:
    :return:
    """
    if low >= high:
        raise ValueError
    total = 0.0
    for line_seg in trajectory_line_segs[low:high]:
        total += math.log(line_seg.length, 2)
    return total


def model_cost_func(partition_line):
    """
    L(H): 描述压缩模型所需要的长度
    :param partition_line:
    :return:
    """
    return math.log(partition_line.length, 2)


def encoding_cost_func(trajectory_line_segs, low, high, partition_line):
    """
    L(D|H): 描述利用压缩模型所编码的数据所需要的长度
    :param trajectory_line_segs:
    :param low:
    :param high:
    :param partition_line:
    :param angular_dist_func:
    :param perpendicular_dist_func:
    :return:
    """
    total_angular = 0.0
    total_perp = 0.0
    for line_seg in trajectory_line_segs[low:high]:
        total_angular += angular_distance(partition_line, line_seg)
        total_perp += perpendicular_distance(partition_line, line_seg)

    return math.log(total_angular + DISTANCE_OFFSET, 2) + math.log(total_perp + DISTANCE_OFFSET, 2)


def get_line_segment_from_points(point_a, point_b):
    """
    从两点中得到一条线段
    :param point_a: Point()
    :param point_b: Point()
    :return: LineSegment()
    """
    return LineSegment(point_a, point_b)


def get_trajectory_line_segment_iterator_adapter(iterator_getter, get_line_segment_from_points_func):
    def _func(list, low, high, get_line_segment_from_points_func=get_line_segment_from_points):
        iterator_getter(list, low, high, get_line_segment_from_points_func)

    return _func


def get_trajectory_line_segment_iterator(list, low, high, get_line_segment_from_points_func):
    """
    从list[low, high]中得到一条轨迹线
    :param list: 点列表 [Point(), ...]
    :param low:  起始位置
    :param high: 终止位置
    :param get_line_segment_from_points_func: 两点成线函数
    :return: 线段list，即轨迹线
    """
    if high <= low:
        raise Exception('high must be greater than low index')

    line_segs = []
    cur_pos = low

    while cur_pos < high:
        line_segs.append(get_line_segment_from_points_func(list[cur_pos], list[cur_pos + 1]))
        cur_pos += 1

    return line_segs
