#! /usr/bin/env bash

function abcli_mlflow_validate() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options="$(xtra dryrun)"
        abcli_show_usage "@mlflow validate$ABCUL[$options]" \
            "validate mlflow."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_eval dryrun=$do_dryrun \
        python3 -m blue_objects.mlflow \
        validate \
        "$@"
}
