"""This python script will return the deployment pipelines, and ids for the SRE Deployments Repo -- @manscaped-dev/<repo>

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import sys
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from icecream import ic

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
ic.disable() # Disable debug mode


def get_releases() -> list[dict]:
    """This function will return the releases for the repo -- @manscaped-dev/<repo>.
    
    Returns:
        list[dict]: The releases for the repo -- @manscaped-dev/manscaped-sre-deploy
    """
    # Let's get a JSON objects of the name, id of the workflows
    _cmd = [
            "gh",
            "release",
            "list",
            "--json",
            "createdAt,isDraft,isLatest,isPrerelease,name,publishedAt,tagName",
        ]
    
    r = subprocess.run(_cmd, check=True, capture_output=True)
    
    if r.returncode != 0:
        print(f"[ERROR] - {r.stderr}")
        sys.exit(1)

    _data = json.loads(r.stdout.decode("utf-8")) # JSON data for ALL the releases in the repository

    return [i for i in _data if any(i.get(k) for k in ("isDraft", "isPrerelease", "isLatest"))]


def get_draft_release(obj: list) -> dict:
    """This function will return the draft release for the repo -- @manscaped-dev/<repo>.
    
    Returns:
        dict: The draft release for the SRE Deployments Repo -- @manscaped-dev/<repo>.
    """
    return next([i for i in obj if i.get("isDraft") == True], None) # Return the draft release


def get_pre_release(obj: list) -> dict:
    """This function will return the prerelease for the Repo -- @manscaped-dev/<repo>.
    
    Returns:
        dict: The prerelease for the repo -- @manscaped-dev/<repo>.
    """
    return next([i for i in obj if i.get("isPrerelease") == True], None) # Return the pre-release


def latest_release(obj: list) -> dict:
    """This function will return the release for the repo -- @manscaped-dev/<repo>.
    
    Returns:
        dict: The release for the repo -- @manscaped-dev/<repo>.
    """
    return next([i for i in obj if i.get("isLatest") == True], None) # Return the latest release


def get_release_id(tagName: str) -> str:
    """This function will return the draft release id for the repo -- @manscaped-dev/<repo>.
    
    Args:
        tagName (str): The tag name for the draft release.

    Returns:
        str: The draft release id for the manscaped-5-server -- @manscaped-dev/<repo>.
    """
    # Let's get the tag name for the draft release
    if (not tagName) or (tagName == "") or (tagName is None):
        print("[ERROR] - The tag name is empty.")
        sys.exit(1)

    _cmd = [
        "gh",
        "release",
        "view",
        tagName,
        "--json",
        "id",
    ]
    r = subprocess.run(_cmd, check=True, capture_output=True)
    if r.returncode != 0:
        print(f"[ERROR] - {r.stderr}")
        sys.exit(1)
    
    _data = json.loads(r.stdout.decode("utf-8")) # JSON data for the release
    
    if _data.get("id"):
        _id = _data.get("id")
    else:
        print("[ERROR] - The id is empty.")
        sys.exit(1)

    return _id # Return the draft release id
