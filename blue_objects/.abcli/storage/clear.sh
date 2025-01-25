#! /usr/bin/env bash

function abcli_storage_clear() {
    :

    cd
    sudo rm -rf $ABCLI_PATH_STORAGE/*
    abcli_select $abcli_object_name
}
