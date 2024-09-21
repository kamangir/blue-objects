#! /usr/bin/env bash

function test_blue_objects_help() {
    local options=$1

    local module
    for module in \
        "abcli_cache" \
        "abcli_clone" \
        "abcli_download" \
        "abcli_gif" \
        "abcli_host" \
        "abcli_metadata" \
        "abcli_mlflow" \
        "abcli_mysql" \
        "abcli_mysql_cache" \
        "abcli_mysql_relations" \
        "abcli_mysql_tags" \
        "abcli_object" \
        "abcli_publish" \
        "abcli_relations" \
        "abcli_select" \
        "abcli_storage" \
        "abcli_tags" \
        "abcli_upload" \
        "blue_objects"; do
        abcli_eval ,$options \
            $module help
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
