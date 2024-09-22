#! /usr/bin/env bash

function abcli_mlflow_set_tags() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options="<keyword-1>=<value>,<keyword-2>,~<keyword-3>"
        abcli_show_usage "@mlflow set_tags$ABCUL[$options]$ABCUL[.|<object-name>]" \
            "set tags in mlflow."
        return
    fi

    local tags=$2

    local object_name=$(abcli_clarify_object $3 .)

    python3 -m blue_objects.mlflow \
        set_tags \
        --object_name $object_name \
        --tags "$tags" \
        "${@:4}"
}
