# This is an SRE tool that will be used to build the prerequisites for the deployment of the application
# The current Shopify application utilizes a TOML file for the configuration of the application
# This script will be used to build the TOML file for the application based on the current environment.

import os
import sys
import toml

BASE = os.path.dirname(os.path.abspath(__file__))
TOML_LOCATION = os.path.abspath(os.path.join(BASE, "..", ".."))
TOML_TEMPLATE = os.path.join(BASE, "shopify.app.toml.template")
TOML_FILE = os.path.join(TOML_LOCATION, "shopify.app.toml")

client_id = str(os.environ.get("CLIENT_ID")) if os.environ.get("CLIENT_ID") else None
extension_name = str(os.environ.get("EXTENSION_NAME")) if os.environ.get("EXTENSION_NAME") else None
extendion_handle = str(os.environ.get("EXTENSION_HANDLE")) if os.environ.get("EXTENSION_HANDLE") else None
shopify_store_url = str(os.environ.get("SHOPIFY_STORE_URL")) if os.environ.get("SHOPIFY_STORE_URL") else None

redirect_urls = [ f"{shopify_store_url}/api/auth" ]

# Let's get our toml file template to render from
with open(TOML_TEMPLATE, "r") as _f:
    toml_string = _f.read()

# Let's ensure that DOPPLER_TOKEN is set
if not os.environ.get("DOPPLER_TOKEN"):
    print("[ERROR] - DOPPLER_TOKEN is not set.")
    print("[CRITICAL] = Please ensure that you have set the DOPPLER_TOKEN environment variable. See your Supervisor/Tech Lead/SRE for more information.")
    sys.exit(1)

def prerequisites():
    if not client_id:
        print("[ERROR] - CLIENT_ID is not set.")
        print("[CRITICAL] - Please ensure that you have set the CLIENT_ID environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not extension_name:
        print("[ERROR] - EXTENSION_NAME is not set.")
        print("[CRITICAL] - Please ensure that you have set the EXTENSION_NAME environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not extendion_handle:
        print("[ERROR] - EXTENSION_HANDLE is not set.")
        print("[CRITICAL] - Please ensure that you have set the EXTENSION_HANDLE environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not shopify_store_url:
        print("[ERROR] - SHOPIFY_STORE_URL is not set.")
        print("[CRITICAL] - Please ensure that you have set the SHOPIFY_STORE_URL environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

    if not redirect_urls:
        print("[ERROR] - REDIRECT_URLS is not set.")
        print("[CRITICAL] - Please ensure that you have set the REDIRECT_URLS environment variable. See your Supervisor/Tech Lead/SRE for more information.")
        sys.exit(1)

def build_toml_file():
    with open(TOML_FILE, "w") as f:
        toml.dump(data, f)

    # Let's add the contextual information at line 1
    with open(TOML_FILE, "r+") as f:
        _data = f.read()
        f.seek(0, 0)
        f.write("# Learn more about configuring your app at https://shopify.dev/docs/apps/tools/cli/configuration\n\n" + _data)

if __name__ == "__main__":
    # Let's check the prerequisites
    prerequisites()

    # Let's load the TOML file
    data = toml.loads(toml_string)
    data["client_id"] = client_id
    data["name"] = extension_name
    data["handle"] = extendion_handle
    data["application_url"] = shopify_store_url
    data["auth"]["redirect_urls"] = redirect_urls

    # Let's build the TOML file
    build_toml_file()
