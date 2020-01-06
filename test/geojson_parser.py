"""
将geojosn数据格式转换成聚类分析的格式
"""

import json

from coordinate import get_all_trajectory_line_segments_iterable_from_all_points_iterable, \
    get_trajectory_line_segments_from_points_iterable, run_traclus
from geometry import Point, LineSegment
from parameter_estimation import TraclusSimulatedAnnealingState, TraclusSimulatedAnnealer
from partition2 import call_partition_trajectory


def read_data_from_file(file_path):
    with open(file_path, 'r') as f:
        data_str = f.read()

    data_dict = json.loads(data_str)
    return data_dict


def get_trajectories_from_data(data_dict):
    """
    :param data_dict:
    :return: 轨迹列表[轨迹点列表]
    """
    features = data_dict['features']
    trajectories_list = []
    for feature in features:
        geometry = feature['geometry']
        trajectory_point_list = []
        if geometry['type'] == 'LineString':
            coordinates = geometry['coordinates']
            for coord in coordinates:
                point = Point(coord[0], coord[1])
                trajectory_point_list.append(point)
                # print(point)
        else:
            pass
        trajectories_list.append(trajectory_point_list)
    return trajectories_list


def read_campus_data():
    """ 读取 校园测试数据
    :return: 轨迹点集合 集合
    """
    with open('raw_campus_trajectories.txt', 'r') as f:
        data = json.loads(f.read())
    trajectories = data['trajectories']
    point_iter_list = []
    for tra in trajectories:
        point_iter = []
        for p in tra:
            point = Point(p['x'], p['y'])
            point_iter.append(point)
        point_iter_list.append(point_iter)
    return point_iter_list


def convert_trajectories_to_geojson(data_format, data):
    geojson = {"type": "FeatureCollection", "features": []}

    if data_format == "point_iter_list":
        for point_iter in data:
            geometry = {"type": "LineString", "coordinates": []}
            feature = {"type": "Feature", "properties": {}, "geometry": geometry}
            for point in point_iter:
                p = [point.y, point.x]
                geometry["coordinates"].append(p)
            geojson["features"].append(feature)

    elif data_format == "line_segment_list":
        for traj_line in data:
            geometry = {"type": "LineString", "coordinates": []}
            feature = {"type": "Feature", "properties": {}, "geometry": geometry}
            point_start = [traj_line.line_segment.start.y, traj_line.line_segment.start.x]
            point_end = [traj_line.line_segment.end.y, traj_line.line_segment.end.x]
            feature["properties"] = {"trajectory_id": traj_line.trajectory_id}
            geometry["coordinates"] = [point_start, point_end]
            geojson["features"].append(feature)

    else:
        raise ValueError("invalid data_format")

    return json.dumps(geojson)


def save_data_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)


def do_test():
    path = 'data.txt'
    data = read_data_from_file(file_path=path)
    print("showing raw data ...")
    trajectories = get_trajectories_from_data(data)
    for tra in trajectories:
        for t in tra:
            print(t)
        print('--------')

    print("showing partition index list ....")
    for tra in trajectories:
        r = call_partition_trajectory(tra)
        print(r)

    print('////////////////')
    print("showing dbscan cluster result ......")
    out_tra = get_all_trajectory_line_segments_iterable_from_all_points_iterable(trajectories)
    print(out_tra)
    geo = convert_trajectories_to_geojson("line_segment_list", out_tra)
    print(geo)
    save_data_to_file("geojson22.txt", geo)


def simulate_annealing():
    input_trajectories = read_campus_data()
    # input_trajectories = [[Point(0, 0), Point(0, 1)], [Point(2, 0), Point(2, 1)], [Point(3, 0), Point(3, 1)]]
    initial_state = TraclusSimulatedAnnealingState(input_trajectories=input_trajectories, epsilon=0.0)
    traclus_sim_anneal = TraclusSimulatedAnnealer(initial_state=initial_state, max_epsilon_step_change=0.000001)
    traclus_sim_anneal.updates = 0
    traclus_sim_anneal.steps = 20
    best_state, best_energy = traclus_sim_anneal.anneal()
    print(best_state.get_epsilon())


if __name__ == '__main__':
    simulate_annealing()

    # point_iter_list = read_campus_data()
    # print(point_iter_list)
    #
    # re = run_traclus(point_iterable_list=point_iter_list, epsilon=0.00016, min_neighbors=2,
    #                  min_num_trajectories_in_cluster=3,
    #                  min_vertical_lines=2, min_prev_dist=0.0002)
    # # re = run_traclus(point_iterable_list=point_iter_list, epsilon=0.00016, min_neighbors=2)
    # print(re)
    #
    # geo = convert_trajectories_to_geojson('point_iter_list', re)
    # print(geo)
