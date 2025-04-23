"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/manscaped-sre-deployments

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import sys
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from icecream import ic
from common import get_releases, get_draft_release, get_pre_release, latest_release # Import the get_releases function from common.py

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
ic.disable() # Disable debug mode

# Let's create an argument parser
parser = argparse.ArgumentParser(
    prog='SRE Deployment Workflow ID',
    description='Returns the deployment workflow id for the pipeline passed in as an argument.'
)
parser.add_argument("--draft", action="store_true", help="Get Draft Release Commit SHA.", default=False) # Dev
parser.add_argument("--prerelease", action="store_true", help="Get Pre-Release Commit SHA.", default=False) # Dev
parser.add_argument("--release", action="store_true", help="Get Latest Release Commit SHA.", default=False) # Dev
parser.add_argument("--debug", action="store_true", help="Enable debug mode.", default=False) # Debug mode


args = parser.parse_args() # Parse the arguments

if args.debug:
    ic.enable() # Enable debug mode

# Let's return the draft release commit sha
def get_release_commit_sha(obj: dict) -> str:
    """This function will return the commit sha for the draft release.
    
    Returns:
        str: The commit sha for the draft release
    """
    _tag = obj.get("tagName") # Get the tag name for the draft release

    if not _tag or _tag == "":
        print("Error: The tag name is empty.")
        sys.exit(1)

    _cmd = [
        "gh",
        "api",
        f"repos/{os.environ.get('GITHUB_REPOSITORY')}/git/refs/tags/{_tag}"
    ]

    r = subprocess.run(_cmd, check=True, capture_output=True)
    if r.returncode != 0:
        print(f"Error: {r.stderr}")
        sys.exit(1)

    _data = json.loads(r.stdout.decode("utf-8")) # JSON data for the release
    
    ic(f"Data: {_data}") # Print the data for the release - debugging purposes

    if _data.get("object").get("sha"):
        _sha = _data.get("object").get("sha") # Get the commit sha for the release
    
    return _sha if _sha else None # If the sha is empty, return an empty string

ic(f"Github Draft Release SHA: {get_release_commit_sha(obj=get_draft_release())}") # debugging purposes

if __name__ == "__main__":
    # Let's get the releases for the repository - This data will be used to get the release information
    _releases = get_releases() # Get the releases for the repository

    if not args.dev and not args.stg and not args.prd:
        raise Exception("Error: Please provide an argument to get the release commit sha.")
    
    # Let's get the release commit sha - either draft, pre-release, or latest releases
    if args.draft:
        _dr = get_draft_release(_releases=_releases) # Get the draft release
        _sha_to_print = get_release_commit_sha(obj=_dr) # Get the draft release commit sha
    
    if args.prerelease:
        _pr = get_pre_release(_releases=_releases)
        _sha_to_print = get_release_commit_sha(obj=_pr)

    if args.release:
        _lr = latest_release(_releases=_releases)
        _sha_to_print = get_release_commit_sha(obj=_lr)


    # Let's print the sha for the release we need to compare
    if _sha_to_print:
        print(_sha_to_print) # Print the draft release commit sha
    else:
        raise Exception("Error: The release commit sha is empty.") # Print an error message
