#! /usr/bin/env bash

function test_abcli_mlflow_validate() {
    local options=$1

    abcli_mlflow_validate "$@"
}

function test_abcli_mlflow_search() {
    local options=$1

    abcli_mlflow_search "$@"
}