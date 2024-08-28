"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script

config = json.load(open(os.path.join(BASE, "config.json"))) # Load the config file

# Let's get the deployment pipelines information from the config
deployment_data = config["deployment_data"]

def get_deployment_pipelines():
    # Let's get a JSON objects of the name, id of the pipelines
    _cmd = [
            "gh",
            "workflow",
            "--repo",
            deployment_data["url"],
            "list",
            '--json=name,id,state',
        ]
    r = subprocess.check_output(_cmd).decode("utf-8").strip()

    return json.loads(r)

if __name__ == "__main__":
  print(get_deployment_pipelines())
