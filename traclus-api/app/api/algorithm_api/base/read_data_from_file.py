import json

from .geometry import Point
from .partitioning import call_partition_trajectory

data_str = ''
with open('raw_campus_trajectories.txt', 'r') as f:
    data_str = f.read()

trajectory_list = json.loads(data_str)['trajectories']

for index, trajectory in enumerate(trajectory_list):
    print('轨迹:', index)
    # trajectory_point_list = []
    # for p in trajectory:
    #     point = Point(p['x'], p['y'])
    #     # print(point)
    #     trajectory_point_list.append(point)
    # print(trajectory_point_list)
    # partition_list = call_partition_trajectory(trajectory_point_list)
# print(trajectory_point_list[0])
point_list = []
for p in trajectory_list[30]:
    print(p)
    point = Point(p['x'], p['y'])
    point_list.append(point)

rl = call_partition_trajectory(point_list)
print(point_list)
print(rl)


print(trajectory_list[0])