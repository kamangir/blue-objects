#! /usr/bin/env bash

function abcli_mlflow_browse() {
    local object_name=$1

    if [[ "$object_name" == "help" ]]; then
        abcli_show_usage "@mlflow browse$ABCUL[.|<object-name>|databricks|host|models]" \
            "browse mlflow."
        return
    fi

    local url="https://tbd"

    if [ "$object_name" == "databricks" ]; then
        url="https://accounts.cloud.databricks.com/"
    elif [ "$object_name" == "host" ]; then
        url=$DATABRICKS_HOST
    elif [ "$object_name" == "models" ]; then
        url="$url/#/models"
    elif [ ! -z "$object_name" ]; then
        object_name=$(abcli_clarify_object $object_name .)

        local experiment_id=$(abcli_mlflow get_id $object_name)
        if [ -z "$experiment_id" ]; then
            abcli_log_error "@mlflow: browse: $object_name: object not found."
            return 1
        fi

        url="$url/#/experiments/$experiment_id"
    fi

    abcli_browse $url
}
