"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script

# Let's create an argument parser
parser = argparse.ArgumentParser(
                    prog='SRE Deployment Pipelines',
                    description='Returns the deployment pipeline id for the pipeline passed in as an argument.'
                    )
parser.add_argument(
    '--name',
    type=str,
    required=True,
    help='The name of the pipeline to get the id for.'
)

args = parser.parse_args() # Parse the arguments

config = json.load(open(os.path.join(BASE, "config.json"))) # Load the config file

# Let's get the deployment pipelines information from the config
deployment_data = config["deployment_data"]

def get_deployment_pipelines() -> list:
    """This function will return the deployment pipelines for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments.

    Returns:
        lists: The deployment pipelines for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deploy
    """
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

def get_pipeline_id() -> int:
    """This function will return the id of the pipeline passed in as an argument.

    Returns:
        int: The id of the pipeline passed in as an argument.
    """
    pipelines = get_deployment_pipelines()
    id = [i["id"] for i in pipelines if i["name"] == args.name][0] # This will return the id of the pipeline, if the name passed in matches one of these

    assert id, f"Pipeline with name {args.name} not found." # If the pipeline is not found, raise an error
    return id

if __name__ == "__main__":
    print(get_pipeline_id())
