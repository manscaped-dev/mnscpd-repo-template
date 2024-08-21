#!/bin/bash
# Author - Philip De Lorenzo

# This script retrieves the current Poetry tag and compares it to what is in Git
# and if the Git tags are not equal, then the logic assumes that the tag must be
# added to Github and does as such.
#
# This tagging script is for single repo Poetry libraries.

set -eo pipefail

[[ -z "${1}" ]] && echo "[ERROR] - No arguments passed into the script..." && exit 1

NAME="${1}"
VERSION=$(poetry version | cut -d" " -f2)
TAG="${NAME}/v${VERSION}"

if [[ -z "${CI}" ]]; then
    set +u
else
    set -u
fi

if [[ ! -z "${CI}" ]] && [[ -z "$1" ]]; then
    echo "[ERROR] - In a CI environment, the current Git tag must be passed into this script."
    exit 1
elif [[ ! -z "${CI}" ]] && [[ ! -z "$1" ]]; then
    if [ "${TAG}" != "${1}" ]; then
        git tag -a ${TAG} -m "Version ${TAG} Automation --> Poetry version bump ${1} ~> ${TAG}"
        git push origin ${TAG}
    else
        echo "[ERROR] - Version ${TAG} already exists in Github..."
        exit 0
    fi
elif [ -z ${CI} ]; then
    set +e
    GITVERSION=$(git describe --tags `git rev-list --tags --max-count=1`)
    set -e

    # Let's ensure that the user knows that this is a github issue
    if [[ "${GITVERSION}" == **"fatal"** ]] || [[ "${GITVERSION}" == "" ]]; then
        echo "[WARNING] - It appears there are NO GitHub tags set in the repo...";
        echo "[INFO] - Setting initial version --> ${TAG}"
        git tag -a ${TAG} -m "Version ${TAG} Automation --> Poetry setting initial tag ~> ${TAG}"
        git push origin ${TAG}
        exit 0
    fi

    # Let's create the tag and push it to the repo
    # If the tags do not match, currently we assume that the TAG is newer...
    if [ "${TAG}" != "${GITVERSION}" ]; then
        git tag -a ${TAG} -m "Version ${TAG} Automation --> Poetry version bump ${GITVERSION} ~> ${TAG}"
    else
        echo "[WARNING] - Version ${TAG} already exists in Github..."
        exit 0
    fi

    git push origin ${TAG}
else
    echo "[ERROR] - Something has went wrong and the script will exit 1"
    exit 1
fi