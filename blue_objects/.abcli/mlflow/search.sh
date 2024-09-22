#! /usr/bin/env bash

function abcli_mlflow_search() {
    local filter_string=$1

    if [[ "$filter_string" == "help" ]]; then
        local args="[--log <0>]"
        abcli_show_usage "@mlflow search$ABCUL<filter-string>$ABCUL$args" \
            "search mlflow for <filter-string>${ABCUL2}https://www.mlflow.org/docs/latest/search-experiments.html."
        return
    fi

    python3 -m blue_objects.mlflow \
        search \
        --filter_string "$2" \
        "${@:3}"
}
