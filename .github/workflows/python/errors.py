"""This is the custom error module for consistent and pertinent messaging.

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""

class generatePackageJsonMissingError(Exception):
    def __init__(self, app: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - {self.app} generatePackageJson key is missing, or is not set to true in project.json"
        print(self.message)
        exit(1)


class JestConfigMissingError(Exception):
    def __init__(self, app: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - {self.app} jest.config-e2e.ts file is missing."
        print(self.message)
        exit(1)

class PackageJSONMissingError(Exception):
    def __init__(self, app: str, target: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - apps/{self.app} has a required target - {target} - missing from the project."
        print(self.message)
        exit(1)

class PackageJSONTargetMissingError(Exception):
    def __init__(self, app: str, target: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - apps/{self.app} has a required target - {target} - missing from the package.json."
        print(self.message)
        exit(1)

class RequiredAppTargetMissingError(Exception):
    def __init__(self, app: str, target: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - apps/{self.app} has a required target - {target} - missing from the project.json."
        print(self.message)
        exit(1)

class RequiredLibTargetMissingError(Exception):
    def __init__(self, lib: str, target: str):
        self.lib = lib
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - libs/{self.lib} has a required target - {target} - missing from the project.json."
        print(self.message)
        exit(1)

class TargetAppMixMatchError(Exception):
    def __init__(self, app: str, target: str):
        self.app = app
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - apps/{self.app} has a mixmatch app for target {target}."
        print(self.message)
        exit(1)

class TargetLibMixMatchError(Exception):
    def __init__(self, lib: str, target: str):
        self.lib = lib
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - libs/{self.lib} has a mixmatch app for target {target}."
        print(self.message)
        exit(1)
