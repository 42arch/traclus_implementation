import collections
import math
from heapq import heappush, heappop

from geometry import LineSegment

max_distance_for_neighbors_in_different_trajectories = 1


class FilteredTrajectory:
    def __init__(self, trajectory, id):
        self.id = id
        self.trajectory = trajectory


class FilteredTrajectoryConnection:
    def __init__(self, start_pt, end_pt, start_traj_id, end_traj_id):
        self.start_pt = start_pt
        self.end_pt = end_pt
        self.start_traj_pt = start_traj_id
        self.end_traj_pt = end_traj_id


class FilteredPointGrapgNode:
    def __init__(self, point, index, original_trajectory_id):
        self.point = point
        self.index = index
        self.original_trajectory_id = original_trajectory_id
        self.neighbor_indices = set()
        self.graph_component_id = None

    def add_neighbor(self, other_node):
        if other_node != self:
            self.neighbor_indices.add(other_node.index)
            other_node.neighbor_indices.add(self.index)

    def get_neighbor_indices(self):
        return self.neighbor_indices

    def get_original_trajectory_id(self):
        return self.original_trajectory_id


# add_other_neighbors_func
# find_other_neighbors_func
def get_find_other_nearby_neighbor_func(max_distance):
    def _func(node_index, pt_graph):
        for temp_node in pt_graph:
            if temp_node.point.distance_to(pt_graph[node_index].point) <= max_distance:
                pt_graph[node_index].add_neighbor(temp_node)

    return _func


def get_find_other_nearby_neighbor(node_index, pt_graph, max_distance):
    for temp_node in pt_graph:
        if temp_node.point.distance_to(pt_graph[node_index].point) <= max_distance:
            pt_graph[node_index].add_neighbor(temp_node)


# find_other_neighbors_func
def dummy_find_other_neighbors_func(pt_node, pt_graph):
    return []


# def build_point_graph(filtered_trajectories, add_other_neighbors_func=None):
#     cur_pt_index = 0
#     pt_graph = []
#
#     for traj in filtered_trajectories:
#         prev_pt_graph_node = None
#         for pt in traj.trajectory:
#             pt_graph.append(FilteredPointGrapgNode(pt, cur_pt_index, traj.id))
#             if prev_pt_graph_node is None:
#                 pt_graph[cur_pt_index].add_neighbor(prev_pt_graph_node)
#             if add_other_neighbors_func is None:
#                 add_other_neighbors_func(node_index=cur_pt_index, pt_graph=pt_graph)
#             prev_pt_graph_node = pt_graph[cur_pt_index]
#             cur_pt_index += 1


def build_point_graph(filtered_trajectories):
    cur_pt_index = 0
    pt_graph = []

    for traj in filtered_trajectories:
        prev_pt_graph_node = None
        for pt in traj.trajectory:
            pt_graph.append(FilteredPointGrapgNode(pt, cur_pt_index, traj.id))
            if prev_pt_graph_node is None:
                pt_graph[cur_pt_index].add_neighbor(prev_pt_graph_node)
            # if add_other_neighbors_func is None:
            #     add_other_neighbors_func(node_index=cur_pt_index, pt_graph=pt_graph)
            get_find_other_nearby_neighbor(node_index=cur_pt_index, pt_graph=pt_graph,
                                           max_distance=max_distance_for_neighbors_in_different_trajectories)
            prev_pt_graph_node = pt_graph[cur_pt_index]
            cur_pt_index += 1


def mark_all_in_same_component(pt_node, component_id, pt_graph, find_other_neighbors_func):
    node_queue = collections.deque()
    node_queue.append(pt_node)

    while len(node_queue) > 0:
        temp_node = node_queue.popleft()

        def queue_adder_func(neighbor_index):
            if pt_graph[neighbor_index].graph_component_id is None:
                pt_graph[neighbor_index].graph_component_id = component_id
                node_queue.append(pt_graph[neighbor_index])
            elif pt_graph[neighbor_index].graph_component_id != component_id:
                raise Exception("graph edges should not be directional")

        for neighbor_index in temp_node.get_neighbor_indices():
            queue_adder_func(neighbor_index)
        for neighbor_index in find_other_neighbors_func(pt_node=temp_node, pt_graph=pt_graph):
            queue_adder_func(neighbor_index)


def compute_graph_component_ids(pt_graph, find_other_neighbors_func):
    next_component_id = 0
    for pt_node in pt_graph:
        if pt_node.graph_component_id is None:
            mark_all_in_same_component(pt_node, next_component_id, pt_graph, find_other_neighbors_func)
            next_component_id += 1


def compute_shortest_path(start_node_index, end_node_index, pt_graph):
    """ 计算最短路径
    :param start_node_index:
    :param end_node_index:
    :param pt_graph:
    :return:
    """

    def pt_pt_distance_for_shortest_path_finding(a_index, b_index, pt_graph):
        pt_a = pt_graph[a_index].point
        pt_b = pt_graph[b_index].point
        return math.pow(pt_a.x - pt_b.x, 2) + math.pow(pt_a.y, pt_b.y, 2)

    priority_queue = []
    distances_from_start = [None] * len(pt_graph)
    distances_from_start[start_node_index] = 0.0
    back_edges = [None] * len(pt_graph)
    heappush(priority_queue, (0.0, start_node_index))

    end_node_reached = False
    while len(priority_queue) > 0:
        temp_node_index = heappop(priority_queue)[1]
        if temp_node_index == end_node_index:
            end_node_reached = True
            break
        for neighbor_index in pt_graph[temp_node_index].get_neighbor_indices():
            temp_dist = pt_pt_distance_for_shortest_path_finding(temp_node_index, neighbor_index, pt_graph) + \
                        distances_from_start[temp_node_index]
            if distances_from_start[neighbor_index] is None or temp_dist < distances_from_start[neighbor_index]:
                distances_from_start[neighbor_index] = temp_dist
                heappush(priority_queue, (temp_dist, neighbor_index))
                back_edges[neighbor_index] = temp_node_index

    if not end_node_reached:
        return None, None

    cur_index = end_node_index
    shortest_path = [end_node_index]
    while cur_index != start_node_index:
        cur_index = back_edges[cur_index]
        shortest_path.append(cur_index)
    shortest_path.reverse()
    return shortest_path, distances_from_start[end_node_index]


def find_nearest_points_to_point(point, pt_graph, max_dist):
    """ 找到所有 一个点的最大距离范围内的的所有点
    :param point:
    :param pt_graph:
    :param distance_func:
    :param max_dist:
    :return:
    """
    nearby_points = []
    for pt_node in pt_graph:
        # if distance_func(point, pt_node.point) < max_dist:
        if point.distance_to(pt_node.point) < max_dist:
            nearby_points.append(pt_node.index)
    return nearby_points


def find_all_possible_connections(start_pt, end_pt, pt_graph, max_dist_to_existing_pt):
    # 寻找所有可能的连接
    near_start_indices = find_nearest_points_to_point(start_pt, pt_graph, max_dist_to_existing_pt)
    near_end_indices = find_nearest_points_to_point(end_pt, pt_graph, max_dist_to_existing_pt)
    possible_connections = []
    for start_index in near_start_indices:
        for end_index in near_end_indices:
            if pt_graph[end_index].graph_component_id == pt_graph[start_index].graph_component_id:
                possible_connections.append((start_index, end_index))
    return possible_connections


def find_shortest_connection(start_pt, end_pt, pt_graph, max_dist_to_existing_pt):
    """ 寻找最短连接
    :param start_pt:
    :param end_pt:
    :param pt_graph:
    :param max_dist_to_existing_pt:
    :return:
    """
    # def pt_pt_distance_func_for_finding_nearby_points(pt_a, pt_b):
    #     return pt_a.distance_to(pt_b)

    # def pt_pt_distance_func_for_shortest_path_finding(a_index, b_index, pt_graph):
    #     pt_a = pt_graph[a_index].point
    #     pt_b = pt_graph[b_index].point
    #     return math.pow(pt_a.x - pt_b.x, 2) + math.pow(pt_a.y, pt_b.y, 2)

    possible_connections = find_all_possible_connections(start_pt=start_pt, end_pt=end_pt, pt_graph=pt_graph,
                                                         max_dist_to_existing_pt=max_dist_to_existing_pt)
    if len(possible_connections) == 0:
        return None, None

    shortest_connection = None
    for connection in possible_connections:
        temp_path, temp_dist = compute_shortest_path(start_node_index=connection[0], end_node_index=connection[1],
                                                     pt_graph=pt_graph)
        if shortest_connection is None or temp_dist < shortest_connection[1]:
            shortest_connection = (temp_path, temp_dist)

    return list(map(lambda i: pt_graph[i].point, shortest_connection[0])), shortest_connection[1]


def get_nearest_point_line_segs(traj, all_trajectories):
    """ 获得最近点的线段
    :param traj:
    :param all_trajectories:
    :return:
    """

    def get_all_points_of_trajectory(trajectory):
        point_list = list(map(lambda x: x.start, list(map(lambda y: y.trajectory, all_trajectories))))
        point_list.append(trajectory.end)
        return point_list

    def get_nearest_point_in_line_segs_to_point(point):
        min_dist_line_seg = None
        min_square_dist = None
        for other_traj in all_trajectories:
            if other_traj.id != traj.id:
                for other_pt in get_all_points_of_trajectory(other_traj):
                    temp_square_dist = math.pow(other_pt.x - point.x, 2) + math.pow(other_pt.y - point.y, 2)
                if min_square_dist is None or temp_square_dist < min_square_dist:
                    min_square_dist = temp_square_dist
                    min_dist_line_seg = LineSegment(point, other_pt)
        return min_dist_line_seg

    nearest_to_start = get_nearest_point_in_line_segs_to_point(traj.trajectory[0].start)
    nearest_to_end = get_nearest_point_in_line_segs_to_point(traj.trajectory[len(traj) - 1].end)

    return list(map(lambda x: FilteredTrajectoryConnection(x), [nearest_to_start, nearest_to_end]))


def find_nearest_points_to_all_trajectory_endpoints(filtered_trajectories):
    nearest_point_line_segments = []

    for traj in filtered_trajectories:
        nearest_point_line_segments.extend(get_nearest_point_line_segs(traj, filtered_trajectories))

    return nearest_point_line_segments
