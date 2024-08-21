#!/usr/bin/env bash
# Author: Philip De Lorenzo <phil.delorenzo@manscaped.com> 
# Description: Check if any markdown files have been modified in the current commit

set -eou pipefail

# Diff HEAD with the previous commit
# shellcheck disable=SC2207
diff=( $(git diff --name-only HEAD^ HEAD) )

# Check if the diff contains any markdown files
if [[ ${diff[*]} =~ .*\.md ]]; then
    return 0
else
    return 1
fi
