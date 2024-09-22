from blue_objects.env import ABCLI_MLFLOW_USERNAME


def to_experiment_name(object_name: str) -> str:
    return f"/Users/{ABCLI_MLFLOW_USERNAME}/{object_name}"


def to_object_name(experiment_name: str) -> str:
    return experiment_name.split("/")[-1]
