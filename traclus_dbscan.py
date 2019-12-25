from distance_functions import perpendicular_distance, angular_distance, parrallel_distance
from generic_dbscan import ClusterCandidate, ClusterCandidateIndex, Cluster, ClusterFactory


class TrajectoryLineSegmentFactory:
    def __init__(self):
        self.next_traj_line_seg_id = 0

    def new_trajectory_line_seg(self, line_segment, trajectory_id):
        if line_segment is None or trajectory_id is None or trajectory_id < 0:
            raise Exception('invalid arguments')
        next_id = self.next_traj_line_seg_id
        self.next_traj_line_seg_id += 1
        return TrajectoryLineSegment(line_segment=line_segment, trajectory_id=trajectory_id, id=next_id)


# 轨迹线段类
class TrajectoryLineSegment(ClusterCandidate):
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
    def get_num_neighbors(self, num_neighbors):
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


class RtreeTrajectoryLineSegmentCandidateIndex(ClusterCandidateIndex):
    pass


# 轨迹簇 类
class TrajectoryCluster(Cluster):
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


BestAvailableClusterCandidateIndex = TrajectoryLineSegmentCandidateIndex
