#! /usr/bin/env bash

function test_blue_objects_mysql_relations() {
    local relation=$(abcli mysql relations list --return_list 1 --count 1 --log 0)
    [[ -z "$relation" ]] && return 1

    abcli mysql relations set \
        $object_1 \
        $object_2 \
        $relation \
        validate
    [[ $? -ne 0 ]] && return 1

    abcli_assert \
        $(abcli mysql relations get $object_1 $object_2) \
        $relation
}
