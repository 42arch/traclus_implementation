from distance_functions import perpendicular_distance, angular_distance, parrallel_distance
import collections


# generic_dbscan
class ClusterCandidate:
    """ 候选簇类  被 TrajectoryLineSegment类 继承 """
    def __init__(self):
        self.cluster = None
        self.__is_noise = False

    def is_classified(self):
        return self.__is_noise or self.cluster is not None

    def is_noise(self):
        return self.__is_noise

    def set_as_noise(self):
        self.__is_noise = True

    def assign_to_cluster(self, cluster):
        self.cluster = cluster
        self.__is_noise = False

    def distance_to_candidate(self, other_candidate):
        raise NotImplementedError()


class ClusterCandidateIndex:
    """ 簇 索引 类 被 TrajectoryLineSegmentCandidateIndex 继承 """
    def __init__(self, candidates, epsilon):
        self.candidates = candidates
        self.epsilon = epsilon

    def find_neighbors_of(self, cluster_candidate):
        neighbors = []
        for item in self.candidates:
            if item != cluster_candidate and cluster_candidate.distance_to_candidate(item) <= self.epsilon:
                neighbors.append(item)
        return neighbors


class Cluster:
    """簇类"""
    def __init__(self):
        self.members = []
        self.members_set = set()

    def add_member(self, item):
        if item in self.members_set:
            raise Exception('item' + str(item) + 'already exists in this cluster')
        self.members_set.add(item)
        self.members.append(item)

    def __repr__(self):
        return str(self.members)


class ClusterFactory:
    @staticmethod
    def new_cluster(self):
        return Cluster()


def dbscan(cluster_candidates_index, min_neighbors, cluster_factory):
    """ 线段聚类算法
    对于一条未分类的线段，计算其邻域判断是否为核心线段。若是，
    :param cluster_candidates_index: 候选簇 下标
    :param min_neighbors:
    :param cluster_factory:
    :return: 返回簇的集合
    """
    clusters = []
    item_queue = collections.deque()

    for item in cluster_candidates_index.candidates:
        if not item.is_classified():
            neighbors = cluster_candidates_index.find_neighbors_of(item)
            # 计算每个簇的基数，若值大于阈值
            if len(neighbors) >= min_neighbors:
                cur_cluster = cluster_factory.new_cluster()  # 当前簇

                cur_cluster.add_member(item)
                item.assign_to_cluster(cur_cluster)

                for other_item in neighbors:
                    other_item.assign_to_cluster(cur_cluster)
                    cur_cluster.add_member(other_item)
                    item_queue.append(other_item)

                expand_cluster(item_queue, cur_cluster, min_neighbors, cluster_candidates_index)
                clusters.append(cur_cluster)
            else:
                item.set_as_noise()  # 小于阈值，将该簇淘汰（设为噪声）
    return clusters


def expand_cluster(item_queue, cluster, min_neighbors, cluster_candidates_index):
    """ 计算一个（线段）密度连接集
    如果新加入的线段为被分类，则把其加入队列item_queue中做进一步扩展，
    若新加入的线段不是核心线段，则不加入到队列中
    :param item_queue:
    :param cluster:
    :param min_neighbors:
    :param cluster_candidates_index:
    :return:
    """

    while len(item_queue) > 0:
        item = item_queue.popleft()
        neighbors = cluster_candidates_index.find_neighbors_of(item)
        if len(neighbors) >= min_neighbors:
            for other_item in neighbors:
                if not other_item.is_classified():
                    item_queue.append(other_item)
                if other_item.is_noise() or not other_item.is_classified():
                    other_item.assign_to_cluster(cluster)
                    cluster.add_member(other_item)


# traclus_dbscan部分
class TrajectoryLineSegmentFactory:
    def __init__(self):
        self.next_traj_line_seg_id = 0

    def new_trajectory_line_seg(self, line_segment, trajectory_id):
        if line_segment is None or trajectory_id is None or trajectory_id < 0:
            raise Exception('invalid arguments')
        next_id = self.next_traj_line_seg_id
        self.next_traj_line_seg_id += 1
        return TrajectoryLineSegment(line_segment=line_segment, trajectory_id=trajectory_id, id=next_id)


class TrajectoryLineSegment(ClusterCandidate):
    """"轨迹线段类"""
    def __init__(self, line_segment, trajectory_id, position_in_trajectory=None, id=None):
        ClusterCandidate.__init__(self)
        if line_segment is None or trajectory_id < 0:
            raise Exception
        self.line_segment = line_segment
        self.trajectory_id = trajectory_id
        self.position_in_trajectory = position_in_trajectory
        self.num_neighbors = -1
        self.id = id

    # 获取邻域线段数量
    def get_num_neighbors(self):
        if self.num_neighbors == -1:
            raise Exception("haven't counted num neighbors yet")
        return self.num_neighbors

    # 设置邻域数量
    def set_num_neighbors(self, num_neighbors):
        if self.num_neighbors != -1 and self.num_neighbors != num_neighbors:
            raise Exception("neighbors count should never be changing")
        self.num_neighbors = num_neighbors

    # 到另一候选轨迹线段的距离
    def distance_to_candidate(self, other_candidate):
        if other_candidate is None or other_candidate.line_segment is None or self.line_segment is None:
            raise Exception()
        return perpendicular_distance(self.line_segment, other_candidate.line_segment) + angular_distance(
            self.line_segment, other_candidate.line_segment) + parrallel_distance(self.line_segment,
                                                                                  other_candidate.line_segment)

    def __repr__(self):
        return str(self.line_segment)


class TrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    def __init__(self, candidates, epsilon):
        ClusterCandidateIndex.__init__(self, candidates, epsilon)

    def find_neighbors_of(self, cluster_candidate):
        neighbors = ClusterCandidateIndex.find_neighbors_of(self, cluster_candidate)
        cluster_candidate.set_num_neighbors(len(neighbors))
        return neighbors


BestAvailableClusterCandidateIndex = TrajectoryLineSegmentCandidateIndex
# class RtreeTrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
#     pass


class TrajectoryCluster(Cluster):
    """轨迹簇 类"""
    def __init__(self):
        Cluster.__init__(self)
        self.trajectories = set()
        self.trajectory_count = 0

    def add_member(self, item):
        Cluster.add_member(self, item)
        if not (item.trajectory_id in self.trajectories):
            self.trajectory_count += 1
            self.trajectories.add(item.trajectory_id)

    def num_trajectories_contained(self):
        return self.trajectory_count

    def get_trajectory_line_segments(self):
        return self.members


class TrajectoryClusterFactory(ClusterFactory):
    def new_cluster(self):
        return TrajectoryCluster()
