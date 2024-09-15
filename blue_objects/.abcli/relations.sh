#! /usr/bin/env bash

function abcli_relations() {
    local task=$(abcli_unpack_keyword $1 help)
    local object_1=$(abcli_clarify_object $2 .)

    if [ "$task" == "help" ]; then
        abcli_show_usage "@relations clone$ABCUL<object-1>$ABCUL<object-2>" \
            "clone <object-1> relations -> <object-2>."

        abcli_show_usage "@relations get$ABCUL<object-1>$ABCUL<object-2>" \
            "get relation between object_1 and object_2."

        abcli_show_usage "@relations list" \
            "list possible relations."

        abcli_show_usage "@relations search$ABCUL<object-name>$ABCUL[--relation <relation>]" \
            "search for all relations of/relation to <object-name>."

        abcli_show_usage "@relations set$ABCUL<object-1>$ABCUL<object-2>$ABCUL<relation>$ABCUL[validate]" \
            "set <object-1> =relation=> <object-2>."

        return
    fi

    if [ "$task" == "clone" ] || [ "$task" == "get" ] || [ "$task" == "set" ]; then
        local object_2=$(abcli_clarify_object $3 .)
    fi

    if [ "$task" == "clone" ]; then
        python3 -m blue_objects.relations \
            clone \
            --object_1 $object_1 \
            --object_2 $object_2 \
            "${@:4}"
        return
    fi

    if [ "$task" == "get" ]; then
        python3 -m blue_objects.relations \
            get \
            --object_1 $object_1 \
            --object_2 $object_2 \
            "${@:4}"
        return
    fi

    if [ "$task" == "list" ]; then
        python3 -m blue_objects.relations \
            list \
            "${@:2}"
        return
    fi

    if [ "$task" == "search" ]; then
        python3 -m blue_objects.relations \
            search \
            --object_1 $object_1 \
            "${@:3}"
        return
    fi

    if [ "$task" == "set" ]; then
        local options=$5
        local do_validate=$(abcli_option_int "$options" validate 0)

        python3 -m blue_objects.relations \
            set \
            --object_1 $object_1 \
            --object_2 $object_2 \
            --relation $4 \
            "${@:6}"

        [[ "$do_validate" == 1 ]] &&
            abcli_log "relations: $object_1 -$(abcli_relations get $object_1 $object_2)-> $object_2"

        return 0
    fi

    abcli_log_error "@relations: $task: command not found."
    return 1
}
