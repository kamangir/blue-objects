#! /usr/bin/env bash

function abcli_mlflow_log_artifacts() {
    local object_name=$1

    if [[ "$object_name" == "help" ]]; then
        abcli_show_usage "@mlflow log_artifacts$ABCUL[.|<object-name>]$ABCUL[<model-name>]" \
            "log artifacts for <object-name> [and register as <model-name>] in mlflow."
        return
    fi

    object_name=$(abcli_clarify_object $object_name .)

    python3 -m blue_objects.mlflow \
        log_artifacts \
        --object_name $object_name \
        --model_name "$2" \
        --path $ABCLI_OBJECT_ROOT/$object_name \
        "${@:3}"
}
