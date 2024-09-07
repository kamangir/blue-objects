#! /usr/bin/env bash

function blue_objects() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        abcli_clone "$@"
        abcli_download "$@"
        abcli_gif "$@"
        abcli_object "$@"
        abcli_publish "$@"
        abcli_select "$@"
        abcli_upload "$@"
        return
    fi

    abcli_generic_task \
        plugin=blue_objects,task=$task \
        "${@:2}"
}

abcli_log $(blue_objects version --show_icon 1)
