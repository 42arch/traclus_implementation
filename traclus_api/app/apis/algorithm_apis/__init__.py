from flask import Blueprint
from flask_restful import Api

from app.apis.algorithm_apis.traclus_api import PartitionResource, ClusterResource, ReplineResource

algorithm = Blueprint('algorithm', __name__)
algorithm_api = Api(algorithm)

algorithm_api.add_resource(PartitionResource, '/partitions/')
algorithm_api.add_resource(ClusterResource, '/clusters/')
algorithm_api.add_resource(ReplineResource, '/rep_lines/')
