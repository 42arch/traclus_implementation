""" 将geojosn数据格式转换成聚类分析的格式 """

import json

from .base.geometry import Point
from .base.parameter_estimation import TraclusSimulatedAnnealingState, TraclusSimulatedAnnealer


def read_data_from_json_file(file_path):
    with open(file_path, 'r') as f:
        json_data = f.read()

    return json_data


def save_data_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)


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


def transform_geojson_to_trajectories(json_data):
    dict_data = json.loads(json_data)
    features = dict_data['features']
    point_iter_list = []
    for feature in features:
        geometry = feature['geometry']
        point_iter = []
        if geometry['type'] == 'LineString':
            coordinates = geometry['coordinates']
            for coord in coordinates:
                point = Point(coord[0], coord[1])
                point_iter.append(point)
        else:
            pass
        point_iter_list.append(point_iter)
    return point_iter_list


def transform_trajectories_to_geojson(data_format, data):
    geojson = {"type": "FeatureCollection", "features": []}

    # 点集集合 格式 (原始数据 point_iter_list)
    if data_format == "point_iter_list":
        for point_iter in data:
            geometry = {"type": "LineString", "coordinates": []}
            feature = {"type": "Feature", "properties": {}, "geometry": geometry}
            for point in point_iter:
                p = [point.x, point.y]
                geometry["coordinates"].append(p)
            geojson["features"].append(feature)
    # 线段集合格式 (分段结果)
    elif data_format == "line_segment_list":
        for traj_line in data:
            geometry = {"type": "LineString", "coordinates": []}
            feature = {"type": "Feature", "properties": {}, "geometry": geometry}
            point_start = [traj_line.line_segment.start.x, traj_line.line_segment.start.y]
            point_end = [traj_line.line_segment.end.x, traj_line.line_segment.end.y]
            feature["properties"] = {"trajectory_id": traj_line.trajectory_id}
            geometry["coordinates"] = [point_start, point_end]
            geojson["features"].append(feature)

    # 轨迹簇 集合格式 （聚类结果）
    elif data_format == "trajectory_cluster_list":
        for index, cluster in enumerate(data):
            for trajectory_line_segment in cluster.get_trajectory_line_segments():
                geometry = {"type": "LineString", "coordinates": []}
                feature = {"type": "Feature", "properties": {}, "geometry": geometry}
                point_start = [trajectory_line_segment.line_segment.start.x,
                               trajectory_line_segment.line_segment.start.y]
                point_end = [trajectory_line_segment.line_segment.end.x,
                             trajectory_line_segment.line_segment.end.y]
                feature["properties"] = {"trajectory_id": trajectory_line_segment.trajectory_id, "cluster_id": index}
                geometry["coordinates"] = [point_start, point_end]
                geojson["features"].append(feature)
    else:
        raise ValueError("invalid data_format")

    return json.dumps(geojson)


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


def simulate_annealing(input_trajectories):
    # input_trajectories = [[Point(0, 0), Point(0, 1)], [Point(2, 0), Point(2, 1)], [Point(3, 0), Point(3, 1)]]
    initial_state = TraclusSimulatedAnnealingState(input_trajectories=input_trajectories, epsilon=0.0)
    traclus_sim_anneal = TraclusSimulatedAnnealer(initial_state=initial_state, max_epsilon_step_change=0.000001)
    traclus_sim_anneal.updates = 0
    traclus_sim_anneal.steps = 20
    best_state, best_energy = traclus_sim_anneal.anneal()
    print(best_state.get_epsilon())

