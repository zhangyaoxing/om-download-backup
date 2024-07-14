#!/usr/bin/env python3
import sys
sys.path.append('./libs')
from requests.auth import HTTPDigestAuth
from utils import *
from om_api import *
from libs import *

LOGGER_NAME = "BackupExporter"
logger = get_logger(LOGGER_NAME)

def export_snapshot(project_id, clusters):
    for c in clusters:
        cluster_name = c
        cid = clusters[c]["id"]
        logger.info("Looking for latest completed snapshot ID of: /%s/%s(%s)" % (project_id, cluster_name, cid))
        snapshots = get_snapshots(project_id, cid)
        for s in snapshots["results"]:
            # The snapshots are sorted by created time decending.
            # Find the first completed snapshot.
            if s["complete"]:
                sid = s["id"]
                logger.info("Creating restore job to download snapshot %s" % sid)
                payload = config["restore_job_config"]
                payload["snapshotId"] = sid
                job = create_restore_job(project_id, cid, payload)
                # For sharded clusters there can be multiple packages to download (for shards and config)
                for batch in job["results"]:
                    # If any security concern, use urlV2 + API Key instead.
                    url = batch["delivery"]["url"]
                    logger.info("Downloading package: %s" % url)
                    # TODO: Download
                    logger.info("Downloading complete.")
                break

if __name__ == "__main__":
    config = load_config()
    backup_clusters = config["backup_clusters"]
    for project_id in backup_clusters: 
        cluster_ids = backup_clusters[project_id]
        target_clusters = get_target_clusters(project_id, cluster_ids)
        export_snapshot(project_id, target_clusters)
