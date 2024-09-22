#! /usr/bin/env bash

export ABCLI_MLFLOW_STAGES="Staging|Production|Archived"

function abcli_mlflow_transition() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options="model=<model-name>,stage=$ABCLI_MLFLOW_STAGES,version=<version>"
        abcli_show_usage "@mlflow transition$ABCUL[$options]$ABCUL[<description>]" \
            "transition <model-name>."
        return
    fi

    local model_name=$(abcli_option "$options" model)
    local stage_name=$(abcli_option_choice "$options" $(echo $ABCLI_MLFLOW_STAGES | tr \| ,) Staging)
    local version=$(abcli_option "$options" version)

    local description="$2"

    python3 -m blue_objects.mlflow \
        transition \
        --model_name "$model_name" \
        --version "$version" \
        --stage_name "$stage_name" \
        --description "$description" \
        "${@:3}"
}
