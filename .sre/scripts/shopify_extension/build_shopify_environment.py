# This is an SRE tool that will be used to build the prerequisites for the deployment of the application
# The current Shopify application utilizes a TOML file for the configuration of the application
# This script will be used to build the TOML file for the application based on the current environment.

import os
import sys

from dopplersdk import DopplerSDK
from pprint import pprint as pp
from dotenv import load_dotenv
from typing import Any

BASE = os.path.dirname(os.path.abspath(__file__))
ENV_LOCATION = os.path.abspath(os.path.join(BASE, "..", ".."))
ENV_TEMPLATE_FILE = os.path.join(ENV_LOCATION, ".env.template")
ENV_FILE = os.path.join(ENV_LOCATION, ".env")

def prerequisites():
    # Let's ensure that DOPPLER_TOKEN is set
    if not os.environ.get("DOPPLER_TOKEN"):
        print("[ERROR] - DOPPLER_TOKEN is not set.")
        print("[CRITICAL] = Please ensure that you have set the DOPPLER_TOKEN environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    # Let's ensure that DOPPLER_PROJECT is set
    if not os.environ.get("DOPPLER_PROJECT"):
        print("[ERROR] - DOPPLER_PROJECT is not set.")
        print("[CRITICAL] = Please ensure that you have set the DOPPLER_PROJECT environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    # Let's ensure that DOPPLER_CONFIG is set
    if not os.environ.get("DOPPLER_CONFIG"):
        print("[ERROR] - DOPPLER_CONFIG is not set.")
        print("[CRITICAL] = Please ensure that you have set the DOPPLER_CONFIG environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not os.environ.get("GITHUB_ACTIONS") or os.environ.get("GITHUB_ACTIONS") != "true":
        print("[ERROR] - This is a local environment, this script can only be run within Github Actions.")
        print("[CRITICAL] = This can only be run within the Github Actions environment. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not os.environ.get("SRE_DOPPLER_TOKEN"):
        print("[ERROR] - SRE_DOPPLER_TOKEN is not set.")
        print("[CRITICAL] = Please ensure that you have set the SRE_DOPPLER_TOKEN environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)


def get_key_names_from_template() -> list:
    """Returns a list of keys from the template file.
    
    This function will read the template file and return a list of keys that are present in the template file.
    This list will be used to build the env file for the application, using the keys and values from Doppler.

    Returns:
        list: A list of keys from the template file.
    """
    keys = []
    template_file = open(ENV_TEMPLATE_FILE, "r").readlines()
    for line in template_file:
        if not line.startswith("#") and "=" in line:
            key = line.split("=")[0].strip()
            keys.append(key)

    return keys


def get_sre_doppler_token():
    return os.environ.get("SRE_DOPPLER_TOKEN")


def get_doppler_api_url():
    return "https://api.doppler.com/v3"


def set_doppler_sdk() -> DopplerSDK:
    token = get_sre_doppler_token()
    doppler = DopplerSDK()
    doppler.set_access_token(token)

    return doppler


def get_doppler_secret(dp: DopplerSDK, name: str) -> DopplerSDK:
    _project = os.environ.get("DOPPLER_PROJECT")
    _config = os.environ.get("DOPPLER_CONFIG")

    secret = dp.secrets.get(project=_project, config=_config, name=name)

    return secret.value["raw"]


def get_doppler_headers(token: str) -> dict:
    """Returns the headers for the Doppler API.

    This function will return the headers that are required to make calls to the Doppler API.
    The headers will contain the authorization token that is required to make calls to the Doppler API.

    Args:
        token (str): The Doppler token that is required to make calls to the Doppler API.

    Returns:
        dict: A dictionary containing the headers required to make calls to the Doppler API.
    """
    headers = {"accept": "application/json", "content-type": "application/json", "authorization": f"Bearer {token}"} # Used by most calls to the Doppler API
    
    return headers


def build_env_file():
    # Let's write an .env from the template
    with open(ENV_FILE, "w+") as f:
        for key, value in secrets.items():
            f.write(f"{key}={value}\n")

    
if __name__ == "__main__":
    # Let's check the prerequisites
    prerequisites()

    _token = os.environ.get("SRE_DOPPLER_TOKEN") # Since the prerequisites have been met, we can safely get the SRE_DOPPLER_TOKEN

    # Let's get the Doppler API URL
    doppler_api_url = get_doppler_api_url()
    headers = get_doppler_headers(token=_token)
    page_count_param = "page=1&per_page=50"

    # Let's build the environment file
    keys: list = get_key_names_from_template()

    # Let's get the secrets from Doppler
    dp = set_doppler_sdk()

    secrets = {} # Let's store the secrets here
    for key in keys:
        secrets.update({key: get_doppler_secret(dp=dp, name=key)}) # Let's get the secret from Doppler, and add it as a key-value pair to the secrets dictionary

    build_env_file() # Let's build the .env file, using the secrets dictionary
