import json
import os

from flask import request, make_response
from flask_restful import Resource, reqparse, abort, fields, marshal

from app.apis.algorithm_apis.traclus.base.coordinate import get_partitioning_result, get_clustering_result, \
    get_rep_line_result
from app.apis.algorithm_apis.traclus.geojson_parser import transform_geojson_to_trajectories, \
    transform_trajectories_to_geojson
from .traclus import geojson_parser

parse_base = reqparse.RequestParser()
parse_base.add_argument('data', type=str, required=True, help='please input geojson string!')

parse_partitioning = parse_base.copy()

parse_clustring = parse_base.copy()
parse_clustring.add_argument('epsilon', type=float, required=True, help='please input the epsilon argument')
parse_clustring.add_argument('min_neighbors', type=int, required=True, help='please input the min_neighbors argument')

parse_traclus = parse_clustring.copy()
parse_traclus.add_argument('min_num_trajectories_in_cluster', type=int, required=True,
                           help="please input the min_num_trajectories argument")
parse_traclus.add_argument('min_vertical_lines', type=int, required=True,
                           help="please input the min_vertical_line argument")
parse_traclus.add_argument('min_prev_dist', type=float, required=True, help="please input the min_prev_dist argument")


class PartitionResource(Resource):
    def get(self):
        pass

    def post(self):
        args_partitioning = parse_partitioning.parse_args()
        json_data = args_partitioning.get('data')
        # json_data = request.form.get('data')
        print(type(json_data))
        trajectories_data = transform_geojson_to_trajectories(json_data)
        partition_result = get_partitioning_result(trajectories_data)
        partition_result_json = transform_trajectories_to_geojson(data_format="line_segment_list",
                                                                  data=partition_result)
        response = make_response(partition_result_json)
        response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000"

        return partition_result_json


class ClusterResource(Resource):
    def get(self):
        pass

    def post(self):
        args_clustering = parse_clustring.parse_args()
        json_data = args_clustering.get('data')
        epsilon = args_clustering.get('epsilon')
        min_neighbors = args_clustering.get('min_neighbors')
        trajectories_data = transform_geojson_to_trajectories(json_data)
        partition_result, clusters = get_clustering_result(point_iterable_list=trajectories_data, epsilon=epsilon,
                                                           min_neighbors=min_neighbors)
        clusters_json = transform_trajectories_to_geojson(data_format="trajectory_cluster_list", data=clusters)

        return clusters_json


class ReplineResource(Resource):
    def get(self):
        pass

    def post(self):
        args_traclus = parse_traclus.parse_args()
        json_data = args_traclus.get('data')
        epsilon = args_traclus.get('epsilon')
        min_neighbors = args_traclus.get('min_neighbors')
        min_num_trajs = args_traclus.get('min_num_trajectories_in_cluster')
        min_vert_lines = args_traclus.get('min_vertical_lines')
        min_prev_dist = args_traclus.get('min_prev_dist')
        trajectories_data = transform_geojson_to_trajectories(json_data)
        partition_res, clusters, replines = get_rep_line_result(point_iterable_list=trajectories_data,
                                                                epsilon=epsilon,
                                                                min_neighbors=min_neighbors,
                                                                min_num_trajectories_in_cluster=min_num_trajs,
                                                                min_vertical_lines=min_vert_lines,
                                                                min_prev_dist=min_prev_dist)
        replines_json = transform_trajectories_to_geojson(data_format="point_iter_list", data=replines)
        return replines_json


# epsilon = 0.06,
# min_neighbors = 8,
# min_num_trajectories_in_cluster = 12,
# min_vertical_lines = 4,
# min_prev_dist = 0.01