"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import sys
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script

config = json.load(open(os.path.join(BASE, "config.json"))) # Load the config file

# Let's get the deployment workflows information from the config
deployment_data = config["deployment_data"]


def get_workflow_data() -> list[dict]:
    """This function will return the deployment workflows for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments.

    Returns:
        lists: The deployment workflows for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deploy

        For example:
        [
            {
                "name": "workflow-name",
                "id": "workflow-id",
                "path": "workflow-path"
            },
            ...
        ]
    """
    # Let's get a JSON objects of the name, id of the workflows
    _cmd = [
            "gh",
            "workflow",
            "list",
            "--repo",
            deployment_data["url"],
            '--json=name,id,path',
        ]

    return json.loads(subprocess.check_output(_cmd).decode("utf-8").strip())

if __name__ == "__main__":
    print(get_workflow_data())
