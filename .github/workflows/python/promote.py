"""This python script will return the deployment pipelines, and ids for the repo -- @manscaped-dev/<repo>

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
import sys
import argparse
import subprocess # We will use subprocess to run the gh command to get the deployment pipelines

from icecream import ic
from common import get_releases, get_draft_release, get_pre_release, latest_release, get_release_id # Import the get_releases function from common.py

BASE = os.path.dirname(os.path.abspath(__file__)) # Get the base directory of the script
ic.disable() # Disable debug mode

# Let's create an argument parser
parser = argparse.ArgumentParser(
    prog='SRE Deployment Workflow ID',
    description='Toggles release(s) for deployment -- Draft to Pre-release -- Pre-release to Latest.'
)
parser.add_argument("--prerelease", action="store_true", help="Get Pre-Release Commit SHA.", default=False) # Dev
parser.add_argument("--release", action="store_true", help="Get Latest Release Commit SHA.", default=False) # Dev
parser.add_argument("--debug", action="store_true", help="Enable debug mode.", default=False) # Debug mode


args = parser.parse_args() # Parse the arguments

if args.debug:
    ic.enable() # Enable debug mode

def cut_prerelease():
    _cmd = [
        "gh",
        "release",
        "edit",
        _draft_release.get("tagName"),
        "--draft=false",
        "--prerelease",
    ]

    r = subprocess.run(_cmd, check=True, capture_output=True)
    if r.returncode != 0:
        print(f"[ERROR] - {r.stderr}")
        sys.exit(1)


def cut_release():
    _cmd = [
        "gh",
        "release",
        "edit",
        _prerelease.get("tagName"),
        "--latest",
        "--draft=false",
        "--prerelease=false",
    ]

    r = subprocess.run(_cmd, check=True, capture_output=True)
    if r.returncode != 0:
        print(f"[ERROR] - {r.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    # Let's get the releases for the repository - This data will be used to get the release information
    _releases: list[dict] = get_releases() # Get the releases for the repository
    ic(f"Releases: {_releases}") # Print the releases - debugging purposes

    if (not args.prerelease) and (not args.release):
        raise Exception("[ERROR] - Please provide a valid argument --prerelease or --release.")
    
    if args.prerelease:
        # This is begins the release process for a draft release (dev) to a pre-release (stg)
        # We MUST have a draft release to process and promote to a pre-release
        _draft_release = get_draft_release(obj=_releases)
        ic(f"Draft Release: {_draft_release}") # Print the draft release - debugging purposes

        release_id = get_release_id(tagName=_draft_release.get("tagName")) # Get the draft release id
        ic(f"Draft Release ID: {release_id}")
        
        _prerelease = get_pre_release(obj=_releases)
        ic(f"Pre-Release: {_prerelease}")

        # Let's check if we have a pre-release, if so, we need to fail as there can be only one
        if _prerelease:
            raise Exception("[ERROR] - The pre-release is not empty.")
        
        # Let's cut the pre-release
        cut_prerelease() # Cut the pre-release
        print("[SUCCESS] - Cutting the pre-release...")


    if args.release:
        # This is begins the release process for a pre-release (stg) to a latest release (prod)
        # We MUST have a pre-release to process and promote to a latest release
        _prerelease = get_pre_release(obj=_releases)
        ic(f"Prerelease: {_prerelease}")

        release_id = get_release_id(tagName=_prerelease.get("tagName")) # Get the draft release id
        ic(f"Prerelease ID: {release_id}")

        if not _prerelease:
            raise Exception("[ERROR] - The pre-release is empty.")
        
        # Let's cut the release
        cut_release()
        print("[SUCCESS] - Cutting the release....")
