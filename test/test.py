from geojson_parser import read_campus_data, read_data_from_json_file, transform_geojson_to_trajectories

from coordinate import get_partitioning_result, get_clustering_result, get_rep_line_result
from geojson_parser import save_data_to_file

from geojson_parser import transform_trajectories_to_geojson

from parameter_estimation import TraclusSimulatedAnnealingState, TraclusSimulatedAnnealer


def simulate_annealing_test(input_trajectories):
    # input_trajectories = [[Point(0, 0), Point(0, 1)], [Point(2, 0), Point(2, 1)], [Point(3, 0), Point(3, 1)]]
    initial_state = TraclusSimulatedAnnealingState(input_trajectories=input_trajectories, epsilon=0.0)
    traclus_sim_anneal = TraclusSimulatedAnnealer(initial_state=initial_state, max_epsilon_step_change=0.001)
    traclus_sim_anneal.updates = 0
    traclus_sim_anneal.steps = 20
    best_state, best_energy = traclus_sim_anneal.anneal()
    print(best_state.get_epsilon())


if __name__ == '__main__':
    ship_json = read_data_from_json_file('aistype_2.json')
    # print(ship_json)
    ship_data = transform_geojson_to_trajectories(ship_json)
    print(ship_data)

    # 模拟退火算法测试
    # simulate_annealing_test(ship_data)

    # partition_result = get_partitioning_result(ship_data)
    # print(partition_result)
    # partition_json = transform_trajectories_to_geojson(data_format="line_segment_list", data=partition_result)
    # print(partition_json)

    # epsilon = 0.0025353096963483053

    # partitioning_result, clustering_result = get_clustering_result(ship_data, epsilon=0.06, min_neighbors=8)
    # print('分段结果', partitioning_result)
    # print('聚类结果', clustering_result)
    #
    # clustering_json = transform_trajectories_to_geojson(data_format="trajectory_cluster_list", data=clustering_result)
    # print(clustering_json)

    partitioning_result, clustering_result, rep_line_result = get_rep_line_result(point_iterable_list=ship_data,
                                                                                  epsilon=0.06,
                                                                                  min_neighbors=8,
                                                                                  min_num_trajectories_in_cluster=12,
                                                                                  min_vertical_lines=4,
                                                                                  min_prev_dist=0.01)
    #
    # print('分段结果', partitioning_result)
    # print('聚类结果', clustering_result)
    # print('代表轨迹', rep_line_result)
    #
    partitioning_json = transform_trajectories_to_geojson(data_format="line_segment_list", data=partitioning_result)
    clustering_json = transform_trajectories_to_geojson(data_format="trajectory_cluster_list", data=clustering_result)
    rep_line_json = transform_trajectories_to_geojson(data_format="point_iter_list", data=rep_line_result)
    save_data_to_file('ship_data/ship_data_partition.json', partitioning_json)
    save_data_to_file('ship_data/ship_data_cluster.json', clustering_json)
    save_data_to_file('ship_data/ship_data_rep_line.json', rep_line_json)
