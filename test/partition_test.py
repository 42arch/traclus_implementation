from coordinate import filter_by_indices, consecutive_item_iterator_getter, \
    get_trajectory_line_segments_from_points_iterable, \
    get_all_trajectory_line_segments_iterable_from_all_points_iterable
from distance_functions import perpendicular_distance
from generic_dbscan import ClusterFactory, ClusterCandidateIndex, dbscan, ClusterCandidate
from geometry import Point, LineSegment
from partition2 import partition_trajectory, call_partition_trajectory
from traclus_dbscan import BestAvailableClusterCandidateIndex
from trajectory import Trajectory
import turtle


# p1 = Point(35.300766422258725, -120.66332459449767)
# p2 = Point(35.3008452273316, -120.66224098205565)
# p3 = Point(35.301221739398365, -120.661758184433)
# p4 = Point(35.30153695745577, -120.6610608100891)
# p4_1 = Point(35.30116044685572, -120.6606638431549)
# p4_2 = Point(35.300573787313, -120.66095352172853)
# p5 = Point(35.300048416948435, -120.66081404685974)
# p6 = Point(35.29983826784755, -120.66045999526976)
# p7 = Point(35.299724436856714, -120.65996646881104)
# p8 = Point(35.30052125043002, -120.65981626510619)

p1 = Point(-120.66332459449767, 35.300766422258725)
p2 = Point(-120.66224098205565, 35.3008452273316)
p3 = Point(-120.661758184433, 35.301221739398365)
p4 = Point(-120.6610608100891, 35.30153695745577)
p4_1 = Point(-120.6606638431549, 35.30116044685572)
p4_2 = Point(-120.66095352172853, 35.300573787313)
p5 = Point(-120.66081404685974, 35.300048416948435)
p6 = Point(-120.66045999526976, 35.29983826784755)
p7 = Point(-120.65996646881104, 35.299724436856714)
p8 = Point(-120.65981626510619, 35.30052125043002)

p11 = Point(0, 0)
p12 = Point(1, 1)

print(p11.distance_to(p12))
print(p1.distance_to(p2))

line_list = [LineSegment(p1, p2), LineSegment(p2, p3), LineSegment(p3, p4), LineSegment(p4, p4_1),
             LineSegment(p4_1, p4_2), LineSegment(p4_2, p5), LineSegment(p5, p6), LineSegment(p6, p7), LineSegment(p7, p8)]
point_list1 = [p1, p2, p3, p4, p4_1, p4_2, p5, p6, p7, p8]
point_list2 = [p1, p2, p3, p4, p5, p6, p7, p8]

p_l_list = [point_list1, point_list2]

# line_a = LineSegment(Point(0, 0), Point(4, 0))
# line_b = LineSegment(Point(0, 3), Point(5, 3))
# print(p1)
p = partition_trajectory(line_list)
r = call_partition_trajectory(point_list1)
r2 = call_partition_trajectory(point_list2)

# print(point_list)
# print(p)
print(r)
print(r2)
out = filter_by_indices(r, point_list1)
# for i in out:
#     print(type(i))
#
out_line = consecutive_item_iterator_getter(out)
# print(out_line)
# for i in out_line:
#     print(i)
# print('///////////////')

out_tra = get_all_trajectory_line_segments_iterable_from_all_points_iterable(p_l_list)
print(out)
for o in out_tra:
    print(o)

clusters = whole_enchilada(p_l_list, 0.0016, 3)
# print(clusters)
print('聚类后....')
for c in clusters:
    print(type(c))
    # print(c.members)
    for i in c.members:
        print(i)
