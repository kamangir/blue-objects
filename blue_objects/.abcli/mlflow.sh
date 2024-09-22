#! /usr/bin/env bash

export MLFLOW_TRACKING_URI="databricks"

function abcli_mlflow() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_mlflow_browse "$@"

        abcli_show_usage "@mlflow clone_tags$ABCUL[..|<object-1>]$ABCUL[.|<object-2>]" \
            "clone mlflow tags."

        abcli_show_usage "@mlflow get_tags$ABCUL[.|<object-name>]" \
            "get mlflow tags for <object-name>."

        abcli_show_usage "@mlflow get_id$ABCUL[.|<object-name>]" \
            "get mlflow id for <object-name>."

        abcli_show_usage "@mlflow list_registered_models" \
            "list mlflow registered models."

        abcli_mlflow_log_artifacts "$@"
        abcli_mlflow_log_run "$@"

        abcli_show_usage "@mlflow rm$ABCUL[.|<object-name>]" \
            "rm <object-name> from mlflow."

        abcli_mlflow_run "$@"

        abcli_mlflow_search "$@"

        abcli_show_usage "@mlflow set_tags${ABCUL}a=b,c=12$ABCUL[.|<object-name>]" \
            "set tags in mlflow."

        abcli_show_usage "@mlflow transition$ABCUL<model-name>$ABCUL<version-1>$ABCUL[Staging/Production/Archived]$ABCUL[<description>]" \
            "transition <model-name>."

        abcli_mlflow_validate "$@"
        return
    fi

    local function_name=abcli_mlflow_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    if [ "$task" == "clone_tags" ]; then
        local source_object=$(abcli_clarify_object $2 ..)
        local destination_object=$(abcli_clarify_object $3 .)

        python3 -m blue_objects.mlflow \
            clone_tags \
            --destination_object $destination_object \
            --source_object $source_object \
            "${@:4}"

        return
    fi

    if [ "$task" == "get_tags" ]; then
        local object_name=$(abcli_clarify_object $2 .)

        python3 -m blue_objects.mlflow \
            get_tags \
            --object_name $object_name \
            "${@:3}"

        return
    fi

    if [ "$task" == "get_id" ]; then
        local object_name=$(abcli_clarify_object $2 .)

        python3 -m blue_objects.mlflow \
            get_id \
            --object_name $object_name \
            "${@:3}"

        return
    fi

    if [ "$task" == "list_registered_models" ]; then
        python3 -m blue_objects.mlflow \
            list_registered_models \
            "${@:2}"
        return
    fi

    if [ "$task" == "rm" ]; then
        local object_name=$(abcli_clarify_object $2 .)

        python3 -m blue_objects.mlflow \
            delete \
            --object_name $object_name \
            "${@:3}"

        return
    fi

    if [ "$task" == "set_tags" ]; then
        local object_name=$(abcli_clarify_object $3 .)

        python3 -m blue_objects.mlflow \
            set_tags \
            --object_name $object_name \
            --tags "$2" \
            "${@:4}"

        return
    fi

    if [ "$task" == "transition" ]; then
        local model_name="$2"
        local version="$3"
        local stage_name=$(abcli_arg_get "$4" Staging)
        local description="$5"

        python3 -m blue_objects.mlflow \
            transition \
            --model_name "$model_name" \
            --version "$version" \
            --stage_name "$stage_name" \
            --description "$description" \
            "${@:6}"

        return
    fi

    abcli_log_error "@mlflow: $task: command not found."
    return 1
}

abcli_source_path - caller,suffix=/mlflow
