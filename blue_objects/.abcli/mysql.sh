#! /usr/bin/env bash

function abcli_mysql() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_mysql_cache "$@"
        abcli_mysql_tags "$@"
        abcli_mysql_relations "$@"
        return
    fi

    local function_name=abcli_mysql_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "@mysql: $task: command not found."
    return 1
}

abcli_source_caller_suffix_path /mysql
