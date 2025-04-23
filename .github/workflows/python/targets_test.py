"""This python script runs the checks for the build workflow.

This will check the project.json files to ensure the needed nx workflows are present.
- lint
- format
- test
- build
- e2e

- Ensures the jest.config-e2e.ts file is present in the apps directory.

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""
import os
import json
from errors import JestConfigMissingError, RequiredAppTargetMissingError, RequiredLibTargetMissingError, TargetAppMixMatchError, TargetLibMixMatchError, PackageJSONMissingError, PackageJSONTargetMissingError

APP_TARGETS = ("lint", "serve", "test", "build", "e2e") # Tuple, this should be immutable through runtime
LIB_TARGETS = ("lint", "test")

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

LIBS_DIR = os.path.join(
    REPO_ROOT,
    "libs"
)


def jest_e2e_check() -> None:
    """This function ensures that the jest.config-e2e.ts file is present in the apps directory.

    Raises:
        JestConfigMissingError: If the jest.config-e2e.ts file is not present in the apps directory.
    """
    for app in os.listdir(APPS_DIR):
        if app == "cloud-functions":
            continue

        print(f"[INFO] - Checking Jest config for {app}...")
        app_dir = os.path.join(APPS_DIR, app)

        if not os.path.isfile(os.path.join(app_dir, "jest.config-e2e.ts")):
            raise JestConfigMissingError(app=app)


def lib_test_target_check(lib: str, obj: str) -> bool:
        """This function checks the e2e target in the project.json file to ensure the correct lib is being used.

        Args:
            app (str): The lib name to check.
            obj (str): The file object to check (open project.json data for the lib).

        Returns:
            bool: True if the correct lib is being used, False otherwise.
        """
        if "outputs" in obj:
            if type(obj["outputs"]) == list:
                for i in obj["outputs"]:
                    if type(i) == str:
                      if "/libs/" in i and f"{lib}" not in i:
                          return False

        if "options" in obj:
            if "jestConfig" in obj["options"]:
                if f"{lib}" not in obj["options"]["jestConfig"]:
                    return False

        return True


def e2e_target_check(app: str, obj: str) -> bool:
        """This function checks the e2e target in the project.json file to ensure the correct app is being used.

        Args:
            app (str): The app name to check.
            obj (str): The file object to check (open project.json data for the app).

        Returns:
            bool: True if the correct app is being used, False otherwise.
        """
        if "outputs" in obj:
            if type(obj["outputs"]) == list:
                for i in obj["outputs"]:
                    if type(i) == str:
                      if "/apps/" in i and f"{app}" not in i:
                          return False

        if "options" in obj:
            if "jestConfig" in obj["options"]:
                if f"{app}" not in obj["options"]["jestConfig"]:
                    return False

        return True


def app_targets_check() -> None:
    """This function checks the project.json files to ensure the needed nx workflows are present (lint, format, test, build, e2e)"""
    for app in os.listdir(APPS_DIR):
      if app == "cloud-functions":
          continue

      print(f"[INFO] - Checking application targets for {app}...")
      app_dir = os.path.join(APPS_DIR, app)

      with open(os.path.join(app_dir, "project.json")) as f:
          project_json = json.load(f)

      for target in APP_TARGETS:
          if target not in project_json["targets"]:
              raise RequiredAppTargetMissingError(app=app, target=target)

          if target == "e2e":
              if not e2e_target_check(app=app, obj=project_json["targets"][target]):
                  raise TargetAppMixMatchError(app=app, target=target)

def app_package_json_check() -> None:
    """This function checks the package.json file to ensure the file exists the needed workflow is present (start)"""
    for app in os.listdir(APPS_DIR):
      if app == "cloud-functions":
          continue

      print(f"[INFO] - Checking project.json targets for {app}...")
      app_dir = os.path.join(APPS_DIR, app)

      if not os.path.isfile(os.path.join(app_dir, "package.json")):
          raise PackageJSONMissingError(app=app, target="package.json")

      with open(os.path.join(app_dir, "package.json")) as f:
          package_json = json.load(f)

      if "start" not in package_json["scripts"]:
          raise PackageJSONTargetMissingError(app=app, target="start")

def lib_targets_check() -> None:
    """This function checks the project.json files to ensure the needed nx workflows are present (lint, format, test)"""
    for lib in os.listdir(LIBS_DIR):
      if lib == "cloud-functions":
          continue

      print(f"[INFO] - Checking library targets for {lib}...")
      lib_dir = os.path.join(LIBS_DIR, lib)

      with open(os.path.join(lib_dir, "project.json")) as f:
          project_json = json.load(f)

      for target in LIB_TARGETS:
          if target not in project_json["targets"]:
              raise RequiredLibTargetMissingError(lib=lib, target=target)

          if target == "test":
              if not lib_test_target_check(lib=lib, obj=project_json["targets"][target]):
                  raise TargetLibMixMatchError(lib=lib, target=target)

print("[INFO] - Running check - jest.config-e2e.ts file locator...")
jest_e2e_check()

print("[INFO] - Running application targets check - project.json files...")
app_targets_check()

print("[INFO] - Running application targets check - package.json files...")
app_package_json_check()

print("[INFO] - Running library targets check - project.json files...")
lib_targets_check()
