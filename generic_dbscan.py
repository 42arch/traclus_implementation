import collections


# 候选簇类
# 被 TrajectoryLineSegment类 继承
class ClusterCandidate:
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


# 簇 索引 类
# 被 TrajectoryLineSegmentCandidateIndex 继承
# (点，邻域e)
class ClusterCandidateIndex:
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
    """
    簇类
    """

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
                item.set_as_noise()   # 小于阈值，将该簇淘汰（设为噪声）
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

