#! /usr/bin/env bash

function abcli_mlflow_tags() {
    local subtask=$1

    if [[ "$subtask" == "help" ]]; then
        abcli_mlflow_tags clone "$@"
        abcli_mlflow_tags get "$@"
        abcli_mlflow_tags search "$@"
        abcli_mlflow_tags set "$@"
        return
    fi

    if [[ "$subtask" == "clone" ]]; then
        if [[ "$2" == "help" ]]; then
            abcli_show_usage "@mlflow tags clone$ABCUL[..|<object-1>]$ABCUL[.|<object-2>]" \
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

        return
    fi

    if [[ "$subtask" == "get" ]]; then
        local object_name=$(abcli_clarify_object $2 .)

        if [[ "$object_name" == "help" ]]; then
            args="[--tag <tag>]"
            abcli_show_usage "@mlflow tags get$ABCUL[.|<object-name>]$ABCUL$args" \
                "get mlflow tags|<tag> for <object-name>."
            return
        fi

        python3 -m blue_objects.mlflow \
            get_tags \
            --object_name $object_name \
            "${@:3}"

        return
    fi

    if [[ "$subtask" == "search" ]]; then
        local filter_string=$2

        if [[ "$filter_string" == "help" ]]; then
            local args="[--delim <space>]$ABCUL[--log <0>]"
            abcli_show_usage "@mlflow tags search$ABCUL<filter-string>$ABCUL$args" \
                "search mlflow for <filter-string>${ABCUL2}https://www.mlflow.org/docs/latest/search-experiments.html."
            return
        fi

        python3 -m blue_objects.mlflow \
            search \
            --filter_string "$filter_string" \
            "${@:3}"

        return
    fi

    if [[ "$subtask" == "set" ]]; then
        if [[ "$2" == "help" ]]; then
            options="<keyword-1>=<value>,<keyword-2>,~<keyword-3>"
            abcli_show_usage "@mlflow tags set$ABCUL[.|<object-name>]$ABCUL[$options]" \
                "set tags in mlflow."
            return
        fi

        local object_name=$(abcli_clarify_object $2 .)

        local tags=$3

        python3 -m blue_objects.mlflow \
            set_tags \
            --object_name $object_name \
            --tags "$tags" \
            "${@:4}"
        return
    fi

    abcli_log_error "@mlflow: tags: $task: command not found."
    return 1
}
