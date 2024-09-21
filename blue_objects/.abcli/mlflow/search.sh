#! /usr/bin/env bash

function abcli_mlflow_search() {
    local filter_string=$1

    if [[ "$filter_string" == "help" ]]; then
        abcli_show_usage "@mlflow search <filter-string>" \
            "search mlflow for <filter-string> - https://www.mlflow.org/docs/latest/search-experiments.html."
        return
    fi

    python3 -m blue_objects.mlflow \
        search \
        --filter_string "$2" \
        "${@:3}"
}
