from flask import Blueprint
from flask_restful import Api

from app.api.algorithm_api.traclus_api import PartitionResource, ClusterResource, ReplineResource
from app.api.algorithm_api.utils_api import FileResource

traclus = Blueprint('traclus', __name__)
traclus_api = Api(traclus)

traclus_api.add_resource(FileResource, '/file')

traclus_api.add_resource(PartitionResource, '/partitions')
traclus_api.add_resource(ClusterResource, '/clusters')
traclus_api.add_resource(ReplineResource, '/rep_lines')
