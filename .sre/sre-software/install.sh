#!/usr/bin/env bash

set -o pipefail

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASEDIR="${BASE}/.."
_GROUP=$(groups | awk -F' ' '{print $1}')

if [[ ! -f "/usr/bin/python" ]]; then
    [[ -f "/usr/bin/python3" ]] && PYTHON=/usr/bin/python3 || echo "[ERROR] - Python is not installed on this system. Please install Python and try again."
fi

asdf_plugin_add()
{
    # Add the plugin in asdf
    asdf plugin add "${1}"
}

install()
{
    cd "${BASEDIR}" || exit 1 && brew update && brew bundle
}

plugins()
{
    # Let's iterate over the .tool-versions file and then install the plugin
    echo "[INFO] - Running asdf plugin additions..."
    while IFS= read -r line; do
        if [[ -n $(echo "${line}" | grep -v '^#' || true) ]]; then
            plugin=$(echo "${line}" | cut -d' ' -f 1)
            # If the plugin is not already installed, install it, else pass
            if [[ -z $(asdf list | grep "${plugin}" || true) ]]; then
                echo "[INFO] - Installing plugin ${plugin}"
                asdf_plugin_add "${plugin}"
            else
                echo "[INFO] - Plugin '${plugin}' is installed already..."
            fi
        fi
    done < "${BASE}/../.tool-versions"

    echo "[INFO] - Running asdf plugin installations..."
    asdf install
}

asdf_installation()
{
    # Let's check for an asdf installation and use that locally
    _asdf=$(command -v asdf)
    # shellcheck disable=SC2236
    if [[ -z ${_asdf} ]]; then
        install # Let's run the asdf installs
        plugins # Let's add and install needed plugins, i.e. ~> Python, Terraform, etc.
    else
        plugins # Let's add and install needed plugins, i.e. ~> Python, Terraform, etc.
    fi
}

python_installation()
{
    ${PYTHON} -m pip install --upgrade pip
    ${PYTHON} -m pip install  --user --break-system-packages -r "${BASE}/python.txt"
    ${PYTHON} -m virtualenv --python=python3.12.6 "${BASEDIR}/.python"
    "${BASEDIR}/.python/bin/pip" install --upgrade pip
    [[ -f "${BASEDIR}/requirements.txt" ]] && "${BASEDIR}/.python/bin/python" -m pip install -r "${BASEDIR}/requirements.txt"
}

completed()
{
    echo "[INFO] - Script complete!"
}

usage() { echo "Usage: $0 [-a asdf][-i install] [-s sops] [-p [Python Install Flag]]" 1>&2; exit 1; }

while getopts "ani:p" arg; do
    case "${arg}" in
        a)
            asdf_installation
            completed
            ;;
        i)
            install
            completed
            ;;
        p)
            python_installation
            completed
            ;;
        \?)
            echo "[ERROR] - Unknown flag passed"
            usage
            ;;
        :)
            echo "[ERROR] - Option -${arg} requires an argument." >&2
            exit 1
            ;;
        *)
            usage
    esac
done

unset_data()
{
    unset _GROUP
    unset BASE
    unset _INFO_NAME
    unset LOCATION
    unset _PUBLICFILENAME
}

# Let's clean up the data.
unset_data

shift $((OPTIND-1))
