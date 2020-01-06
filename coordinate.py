from generic_dbscan import dbscan
from line_segment_averaging import get_representative_line_from_trajectory_line_segments
from partition2 import call_partition_trajectory, get_line_segment_from_points
from traclus_dbscan import BestAvailableClusterCandidateIndex, TrajectoryLineSegmentFactory, TrajectoryClusterFactory


def run_traclus(point_iterable_list, epsilon, min_neighbors, min_num_trajectories_in_cluster, min_vertical_lines,
                min_prev_dist):
    # cleaned_input = []
    # for traj in map(lambda l: with_spikes_removed(l), point_iterable_list):
    #     cleaned_traj = []
    #     if len(traj) > 1:
    #         prev = traj[0]
    #         cleaned_traj.append(traj[0])
    #         for pt in traj[1:]:
    #             if prev.distance_to(pt) > 0.0:
    #                 cleaned_traj.append(pt)
    #                 prev = pt
    #         if len(cleaned_traj) > 1:
    #             cleaned_input.append(cleaned_traj)
    # cleaned_input = clean_trajectories(point_iterable_list=point_iterable_list)
    return almost_done(point_iterable_list=point_iterable_list, epsilon=epsilon, min_neighbors=min_neighbors,
                       min_num_trajectories_in_cluster=min_num_trajectories_in_cluster,
                       min_vertical_lines=min_vertical_lines,
                       min_prev_dist=min_prev_dist, clusters_hook=None)
    # return get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list=cleaned_input)


def clean_trajectories(point_iterable_list):
    """ 轨迹数据清理 """
    cleaned_input = []
    for traj in map(lambda l: with_spikes_removed(l), point_iterable_list):
        cleaned_traj = []
        if len(traj) > 1:
            prev = traj[0]
            cleaned_traj.append(traj[0])
            for pt in traj[1:]:
                if prev.distance_to(pt) > 0.0:
                    cleaned_traj.append(pt)
                    prev = pt
            if len(cleaned_traj) > 1:
                cleaned_input.append(cleaned_traj)
    return cleaned_input


def with_spikes_removed(trajectory):
    if len(trajectory) <= 2:
        return trajectory[:]

    spikes_removed = [trajectory[0]]
    cur_index = 1
    while cur_index < len(trajectory) - 1:
        if trajectory[cur_index - 1].distance_to(trajectory[cur_index + 1]) > 0.0:
            spikes_removed.append(trajectory[cur_index])
        cur_index += 1
    spikes_removed.append(trajectory[cur_index])
    return spikes_removed


def almost_done(point_iterable_list, epsilon, min_neighbors, min_num_trajectories_in_cluster, min_vertical_lines,
                min_prev_dist, clusters_hook):
    cleaned_input = clean_trajectories(point_iterable_list=point_iterable_list)
    # 1. 计算分段后 的轨迹线段集合
    all_traj_segs_iter_from_all_points = get_all_trajectory_line_segments_iterable_from_all_points_iterable(
        point_iterable_list=cleaned_input)
    # 2. 对轨迹线段集合 计算， 得到轨迹簇

    clusters = get_cluster_iterable_from_all_points_iterable(all_traj_segs_iter_from_all_points, epsilon, min_neighbors)
    if clusters_hook:
        clusters_hook(clusters)
    # return clusters

    # 3. 获得代表性轨迹
    rep_lines = get_representative_lines_from_trajectory(clusters=clusters,
                                                         min_num_trajectories_in_cluster=min_num_trajectories_in_cluster,
                                                         min_vertical_lines=min_vertical_lines,
                                                         min_prev_dist=min_prev_dist)
    return rep_lines


def get_cluster_iterable_from_all_points_iterable(cluster_candidates, epsilon, min_neighbors):
    # dbscan()
    line_seg_index = BestAvailableClusterCandidateIndex(candidates=cluster_candidates, epsilon=epsilon)
    clusters = dbscan(cluster_candidates_index=line_seg_index, min_neighbors=min_neighbors,
                      cluster_factory=TrajectoryClusterFactory())
    return clusters


# def get_representative_lines_from_trajectory(trajectory_line_segs, min_vertical_lines, min_prev_dist):
#     return get_representative_line_from_trajectory_line_segments(trajectory_line_segments=trajectory_line_segs,
#                                                                  min_vertical_lines=min_vertical_lines,
#                                                                  min_prev_dist=min_prev_dist)


def get_representative_lines_from_trajectory(clusters, min_num_trajectories_in_cluster, min_vertical_lines,
                                             min_prev_dist):
    rep_lines = []
    for traj_cluster in clusters:
        if traj_cluster.num_trajectories_contained() >= min_num_trajectories_in_cluster:
            rep_line = get_representative_line_from_trajectory_line_segments(
                trajectory_line_segments=traj_cluster.get_trajectory_line_segments(),
                min_vertical_lines=min_vertical_lines,
                min_prev_dist=min_prev_dist)
            rep_lines.append(rep_line)
    return rep_lines


def partition_trajectory():
    pass


def get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list):
    """ 从点集合 的集合中获取全部 分段后的 轨迹线段
    :param point_iterable_list:  轨迹线 点集合（一条轨迹） 的 集合
    :return: list [TrajectoryLineSegment...]
    """
    out = []
    cur_trajectory_id = 0
    for point_trajectory in point_iterable_list:
        line_segments = get_trajectory_line_segments_from_points_iterable(point_iterable=point_trajectory,
                                                                          trajectory_id=cur_trajectory_id)
        temp = 0
        for traj_seg in line_segments:
            out.append(traj_seg)
            temp += 1
        if temp <= 0:
            raise Exception()
        cur_trajectory_id += 1
    return out


def get_trajectory_line_segments_from_points_iterable(point_iterable, trajectory_id):
    """ 从一组原始点 集合中获取 一条分段后的轨迹
    :param point_iterable:
    :param trajectory_id:
    :return: TrajectoryLineSegment
    """
    good_indices = call_partition_trajectory(point_iterable)
    good_point_iterable = filter_by_indices(good_indices=good_indices, vals=point_iterable)
    line_segs = consecutive_item_iterator_getter(item_iterable=good_point_iterable)

    def _create_traj_line_seg(line_seg):
        return TrajectoryLineSegmentFactory().new_trajectory_line_seg(line_segment=line_seg,
                                                                      trajectory_id=trajectory_id)

    return list(map(_create_traj_line_seg, line_segs))


# 根据下标过滤
# 猜测是从分段的点下标集合中得到轨迹点
def filter_by_indices(good_indices, vals):
    """ 从分段算法得到的下标集合中得到 对应的轨迹点集合
    :param good_indices: 下标集合
    :param vals: 原始点数据（未分段） 集合
    :return: 分段后的点集合
    """
    vals_iter = iter(vals)
    good_indices_iter = iter(good_indices)
    out_vals = []

    num_vals = 0
    for i in good_indices_iter:
        if i != 0:
            raise ValueError("the first index should be 0, but it was " + str(i))  # 起点必须为0下标
        else:
            for item in vals_iter:
                out_vals.append(item)
                break
            num_vals = 1
            break

    max_good_index = 0
    vals_cur_index = 1

    for i in good_indices_iter:
        max_good_index = i
        for item in vals_iter:
            num_vals += 1
            if vals_cur_index == i:
                vals_cur_index += 1
                out_vals.append(item)
                break
            else:
                vals_cur_index += 1
    for i in vals_iter:
        num_vals += 1
    if num_vals < 2:
        raise ValueError("list passed in is too short")
    # 分段下标集合最大下标一定是 点集合最后一个
    if max_good_index != num_vals - 1:
        raise ValueError("last index is " + str(max_good_index) + " but there were " + str(num_vals) + " vals")
    # print(max_good_index, num_vals)
    return out_vals


def consecutive_item_iterator_getter(item_iterable):
    """ 从分段的点 集合中 得到连续的线段
    :param item_iterable: 分段后的点集合
    :return: 分段后的线段集合
    """
    # get_line_segment_from_points
    out_vals = []
    iterator = iter(item_iterable)
    last_item = None
    num_items = 0
    for item in iterator:
        num_items = 1
        last_item = item
        break
    if num_items == 0:
        raise ValueError("iterator doesn't have any values")

    for item in iterator:
        num_items += 1
        line_seg = get_line_segment_from_points(last_item, item)
        out_vals.append(line_seg)
        last_item = item

    if num_items < 2:
        raise ValueError("iterator didn't have at least two items")
    return out_vals
