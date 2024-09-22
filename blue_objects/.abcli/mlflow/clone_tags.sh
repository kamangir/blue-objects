#! /usr/bin/env bash

function abcli_mlflow_clone_tags() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options="-"
        abcli_show_usage "@mlflow clone_tags$ABCUL[$options]$ABCUL[..|<object-1>]$ABCUL[.|<object-2>]" \
            "clone mlflow tags."
        return
    fi

    local source_object=$(abcli_clarify_object $2 ..)
    local destination_object=$(abcli_clarify_object $3 .)

    abcli_log "mlflow: tags: clone: $source_object -> $destination_object ..."

    python3 -m blue_objects.mlflow \
        clone_tags \
        --destination_object $destination_object \
        --source_object $source_object \
        "${@:4}"
}
