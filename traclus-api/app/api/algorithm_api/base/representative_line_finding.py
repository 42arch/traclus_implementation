from .geometry import Vector, LineSegment


def get_average_vector(line_segment_list):
    """ 计算线段的平均走向
    将所有向量相加并单位化
    :param line_segment_list:
    :return:
    """

    if len(line_segment_list) < 1:
        raise Exception("tried to get average vector of an empty line segment list")

    total_x = 0.0
    total_y = 0.0
    for segment in line_segment_list:
        if segment.end.x < segment.start.x:
            total_x += segment.start.x - segment.end.x
        else:
            total_x += segment.end.x - segment.start.x
        total_y += segment.end.y - segment.start.y

    return Vector(total_x, total_y)


def get_rotated_line_segment(line_segment, angle_in_degrees):
    """ 坐标系旋转
    如果扫描直线与x轴所成角度不为90°的整数倍，则将坐标系旋转是x轴与平均走向平行
    :param line_segment:
    :param angle_in_degrees:
    :return:
    """
    if angle_in_degrees > 90.0 or angle_in_degrees < -90.0:
        raise Exception("trying to rotate line segment by an illegal number of degrees: " + str(angle_in_degrees))

    new_start = line_segment.start.rotated(angle_in_degrees)
    new_end = line_segment.end.rotated(angle_in_degrees)

    return LineSegment.from_tuples((new_start.x, new_start.y), (new_end.x, new_end.y))
