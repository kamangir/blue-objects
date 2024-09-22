#! /usr/bin/env bash

function test_blue_objects_mlflow_validate() {
    local options=$1

    abcli_mlflow_validate "$@"
}
