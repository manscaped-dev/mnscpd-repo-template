import os
import json
import argparse


### Constants
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
NEGATIONS = [
    "strapi-pim",
    "shopify-webhooks-cli",
    "cloud-functions",
    "honeypot"
]
PROD_NEGATIONS = [
    "mock-api-service"
]

### Configurations
parser = argparse.ArgumentParser(description='Toggle production list of applications')
parser.add_argument('--prod', action='store_true', help='List only production applications', default=False)

args = parser.parse_args()

### Functions
app_list = []
if args.prod:
    for i in os.listdir(APPS_DIR):
        if i in NEGATIONS or i in PROD_NEGATIONS:
            continue

        app_list.append(i)
else:
    for i in os.listdir(APPS_DIR):
        if i in NEGATIONS:
            continue

        app_list.append(i)

print(json.dumps(app_list))
