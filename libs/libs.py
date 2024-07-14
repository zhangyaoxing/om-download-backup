import logging
import os
from om_api import *
from utils import *

TYPE_NAME = {
    "SHARDED_REPLICA_SET": "SHARDED_REPLICA_SET",
    "CONFIG_SERVER_REPLICA_SET": "CONFIG_SERVER_REPLICA_SET",
    "REPLICA_SET": "REPLICA_SET"
}
LOGGER_NAME = "Libs"
logger = get_logger(LOGGER_NAME)

# The clusters returned by API includes the sharded cluster and all its shards and config.
# We need to reorganize them to refect the architecture.
# clusterName is used to recognize shards and config.
def analyse_clusters(all_clusters):
    target_clusters = {}
    for c in all_clusters:
        cluster_name = c["clusterName"]
        type_name = c["typeName"]
        if type_name == TYPE_NAME["SHARDED_REPLICA_SET"]:
            target_clusters[cluster_name] = c
            c["sub_clusters"] = []
    for c in all_clusters:
        cluster_name = c["clusterName"]
        type_name = c["typeName"]
        if type_name != TYPE_NAME["SHARDED_REPLICA_SET"]:
            cluster = target_clusters.get(cluster_name)
            if cluster == None:
                target_clusters[cluster_name] = c
            else:
                cluster["sub_clusters"].append(c)

    logger.debug(target_clusters)
    return target_clusters

# In the config it's allowed to only specify project IDs without specifying cluster IDs.
# This function check if cluster_ids are provided.
# If provided, return the cluster info of each cluster.
# If not provided, return all clusters in the project.
# The result will be in a key/value form where key is the cluster name and value is the cluster info returned by OM.
def get_target_clusters(project_id, cluster_ids):
    all_clusters = []
    # Always get all clusters and reorganize by cluster name
    json = get_clusters(project_id)
    logger.debug(json)
    all_clusters = json["results"]
    target_clusters = analyse_clusters(all_clusters)
    if len(cluster_ids) != 0: 
        # Only need some clusters. Filter by cluster ID.
        to_be_deleted = []
        for cluster_name in target_clusters:
            cluster = target_clusters[cluster_name]
            cid = cluster["id"]
            if not cid in cluster_ids:
                to_be_deleted.append(cluster_name)
        for cluster_name in to_be_deleted:
            del target_clusters[cluster_name]
           
    return target_clusters