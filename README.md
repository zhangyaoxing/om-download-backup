# Download Backup
This is a example of how to download the backups made by Ops Manager.

## Dependencies
```bash
pip3 install requests
```

## Config File
The folowing config settings can be defined:
- `public_key`: Ops Manager API public key.
- `private_key`: Ops Manager API private key.
- `om_url`: Ops Manager base URL.
- `backup_clusters`: Backup of these clusters will be saved.
  - Each key in the sub document is a project ID.
    - Each array element under the project ID is a clusterID. If empty, all clusters are included.
- `restore_job_config`: The script download the backup by creating a restore job. This section configures the restore job.
  - `delivery.expirationHours`: Expiration time of the job.
  - `delivery.maxDownloads`: How many times the backup can be downloaded.
  - `delivery.methodName`: How to download the backup.

## Usage
```bash
./download-backup.py
```

To avoid saving the plaintext keys, you can provide them in the environment variables:
```bash
export public_key="..."
export private_key="..."
./download-backup.py
```

If you want verbose log, set the `--logLevel`:
```bash
./download-backup.py --logLevel=DEBUG
```

## Example Responsesautomation-config/get-automation-config/)
- `get_clusters.json`: [Get All Clusters in One Project](https://www.mongodb.com/docs/ops-manager/current/reference/api/clusters/clusters-get-all/)
- `target_clusters.json`: Because the get all clusters response from Ops Manager will return not only top level clusters, but also shards and config servers. We only need the top level ones in most cases. The function `get_target_clusters` will return the top level ones. This is an example of the response of this function.