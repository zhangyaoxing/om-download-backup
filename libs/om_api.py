from utils import load_config, get_logger
from requests.auth import HTTPDigestAuth
from http import HTTPStatus
import requests

logger_name = "OMAPI"
logger = get_logger(logger_name)
def api_call(resource, method = "GET", payload = {}):
    config = load_config()
    url = config["api_base_url"] + resource
    auth = HTTPDigestAuth(config["public_key"], config["private_key"])
    if method == "GET":
        result = requests.get(url, auth = auth)
    elif method == "POST":
        result = requests.post(url, auth = auth, json = payload)
    elif method == "PUT":
        result = requests.put(url, auth = auth, json = payload)
    if result.status_code != HTTPStatus.OK:
        logger.error("Error returned by server: %s" % result.content)
        exit()

    return result.json()

def get_project(project_id):
    return api_call("/groups/%s" % project_id)

def get_clusters(project_id):
    return api_call("/groups/%s/clusters" % project_id)

def get_snapshots(project_id, cluster_id):
    return api_call("/groups/%s/clusters/%s/snapshots" % (project_id, cluster_id))

def create_restore_job(project_id, cluster_id, payload):
    return api_call("/groups/%s/clusters/%s/restoreJobs" % (project_id, cluster_id), method="POST", payload=payload)
