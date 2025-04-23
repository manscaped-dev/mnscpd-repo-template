"""This python script runs the checks for the build workflow.

- Package JSON check - ensures the package.json file is present, and the generatePackageJson key is set to true.

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
from errors import generatePackageJsonMissingError

BASE = os.path.dirname(
    os.path.abspath(__file__)
)

REPO_ROOT = os.path.abspath(
    os.path.join(
        BASE,
        "..",
        "..",
        ".."
    )
)

APPS_DIR = os.path.join(
    REPO_ROOT,
    "apps"
)

def check_production_configurations(app: str) -> int:
    app_dir = os.path.join(APPS_DIR, app)

    with open(os.path.join(app_dir, "project.json"), "r") as f:
        project_json = json.load(f)

    try:
      if project_json["targets"]["build"]["configurations"]["production"]:
        if "generatePackageJson" in project_json["targets"]["build"]["configurations"]["production"]:
          if project_json["targets"]["build"]["configurations"]["production"]["generatePackageJson"] == True:
            return 1
    except KeyError:
      pass

    return 0


def check_build_options(app: str) -> int:
    app_dir = os.path.join(APPS_DIR, app)

    with open(os.path.join(app_dir, "project.json"), "r") as f:
        project_json = json.load(f)

    try:
      if project_json["targets"]["build"]["options"]:
        if "generatePackageJson" in project_json["targets"]["build"]["options"]:
          if project_json["targets"]["build"]["options"]["generatePackageJson"] == True:
            return 1
    except KeyError:
      pass

    try:
      if project_json["targets"]["build-original"]["options"]:
        if "generatePackageJson" in project_json["targets"]["build-original"]["options"]:
          if project_json["targets"]["build-original"]["options"]["generatePackageJson"] == True:
            return 1
    except KeyError:
      pass

    return 0


def package_json_check() -> None:
    """Check if the package.json file is present and the generatePackageJson key is set to true."""
    for app in os.listdir(APPS_DIR):
        found = 0
        if app == "cloud-functions":
            continue

        print(f"[INFO] - Checking {app}...")
        app_dir = os.path.join(APPS_DIR, app)

        if not os.path.isfile(os.path.join(app_dir, "project.json")):
            raise FileNotFoundError(f"[ERROR] - project.json file not found in {app_dir}")

        if not os.path.isfile(os.path.join(app_dir, "package.json")):
            print(f"[WARNING] - package.json file not found in {app_dir}")

        found += check_build_options(app)
        found += check_production_configurations(app)

        if found == 0:
          generatePackageJsonMissingError(
             app=app
          )


# Run the checks
package_json_check()
