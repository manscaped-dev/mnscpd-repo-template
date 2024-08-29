"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import sys
import time
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script

# Let's create an argument parser
parser = argparse.ArgumentParser(
    prog='SRE Deployment Workflow Job Number',
    description='Returns the deployment workflow job number for the workflow ID passed in as an argument.'
)

parser.add_argument(
    '--workflow_id',
    type=str,
    required=True,
    help='The workflow id to get the job number for.'
)

args = parser.parse_args() # Parse the arguments

config = json.load(open(os.path.join(BASE, "config.json"))) # Load the config file

# Let's get the deployment workflows information from the config
deployment_data = config["deployment_data"]

def current_running_job_list() -> list[dict]:
    """Get a list of current running jobs for the workflow id passed in as an argument.

    Returns:
        list: The current running jobs for the workflow id passed in as an argument.
    """
    # Let's get a JSON objects of the name, id of the workflows
    # gh run list --workflow <workflow-id> --repo <repo-url> --status=queued --status=in_progress --status=waiting --status=requested --json=databaseId,conclusion,createdAt,number,status,updatedAt,url,headBranch,headSha,name
    count = 0
    while count < 10:
        _cmd = [
            "gh",
            "run",
            "list",
            "--workflow",
            args.workflow_id,
            "--repo",
            deployment_data["url"],
            f"--status=in_progress",
            "--json=databaseId,conclusion,createdAt,number,status,updatedAt,url,headBranch,headSha,name"
        ]

        r = json.loads(subprocess.check_output(_cmd).decode("utf-8").strip())
        
        if not r:
            time.sleep(5)
            count += 1
        else:
            break

    return r # Return the current running job list, already loaded as a JSON object


def filter_job_list(job_list: list) -> list:
    """Filter out the current running job from the job list.

    Args:
        job_list (list): The list of jobs to filter.

    Returns:
        list: The filtered list of jobs.
    """
    current_time = datetime.now(tzinfo=timezone.utc)

    # To locate the closet job to this current time, we need to evaluate the epoch time of the created time, and compare to now
    _locate_job = {} # This will create the empty dictionary to locate the job
    for i in job_list:
        created_at = i["createdAt"]
        created_epoch = iso_to_epoch(created_at)

        now = current_time.strftime("%Y%m%dT%H%M%SZ")
        now_epoch = iso_to_epoch(now)

        # Let's convert the created time to a datetime object
        time_delta = now_epoch - created_epoch
        _locate_job.update({time_delta: job_list.index(i)})

    # Let's get the job with the smallest time delta
    deltas = list(_locate_job.keys())
    smallest_delta = __builtins__.min(deltas) # Get the smallest time delta = the closest job to the current time
    job_index = _locate_job[smallest_delta] # Get the index of the job with the smallest time delta

    return job_list[job_index] # Return the job with the smallest time delta


def iso_to_epoch(iso_date):
    """Converts an ISO 8601 date string to an epoch timestamp (seconds since 1970-01-01T00:00:00Z)."""

    dt = datetime.fromisoformat(iso_date)
    return int(dt.replace(tzinfo=timezone.utc).timestamp())


if __name__ == "__main__":
    # The time format returned from the API is ISO 8601 format YYYY-MM-DDTHH:MM:SSZ
    # These are the current runs with the status of queued, in_progress, waiting, requested
    current_running_job_list = current_running_job_list() # Get the current running job list

    if len(current_running_job_list) > 1:
        filtered_job_list = filter_job_list(current_running_job_list) # Filter out the current running job

    elif len(current_running_job_list) == 1:
        filtered_job_list = current_running_job_list
    else:
        print("No runs found.")
        sys.exit(5)

    assert len(filtered_job_list) == 1, "The filter could not filter out the specific job."

    # Let's convert the created time to a datetime object
    print(filtered_job_list[0]["databaseId"])
