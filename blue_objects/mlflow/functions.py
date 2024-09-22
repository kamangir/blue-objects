from typing import Tuple, Dict, List
import os
import glob
import copy
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

from blue_options.options import Options
from blue_options import string
from blue_options.logger import crash_report
from blue_objects import file

from blue_objects.mlflow.objects import to_experiment_name, to_object_name
from blue_objects.logger import logger


def rm(
    object_name: str,
    is_id: bool = False,
) -> bool:
    if is_id:
        experiment_id = object_name
    else:
        experiment_name = to_experiment_name(object_name)

        success, experiment_id = get_id(experiment_name)
        if not success:
            return success

    try:
        client = MlflowClient()

        # get list of run_ids

        # delete all runs

        client.delete_experiment(experiment_id)
    except:
        crash_report("mlflow.rm({})".format(object_name))
        return False

    logger.info(
        "🚮 {}".format(
            "#{}".format(experiment_id)
            if is_id
            else "{} (#{})".format(object_name, experiment_id)
        )
    )

    return True


def get_run_id(
    object_name: str,
    count: int = -1,
    offset: int = 0,
    create: bool = False,
) -> Tuple[bool, List[str]]:
    success, experiment_id = get_id(object_name, create=create)
    if not success:
        return False, []

    try:
        client = MlflowClient()

        list_of_runs = client.search_runs(
            experiment_ids=[experiment_id],
            run_view_type=ViewType.ACTIVE_ONLY,
            max_results=count + offset,
        )

        return True, [run._info.run_id for run in list_of_runs][offset:]

    except:
        crash_report(f"mlflow.get_run_id({object_name})")
        return False, []


def get_tags(
    object_name: str,
) -> Tuple[bool, Dict[str, str]]:
    experiment_name = to_experiment_name(object_name)

    try:
        client = MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)

        if experiment is None:
            return True, {}

        return True, copy.deepcopy(experiment.tags)
    except:
        crash_report("mlflow.get_tags({})".format(object_name))
        return False, {}


def get_id(
    object_name: str,
    create: bool = False,
) -> Tuple[bool, str]:
    experiment_name = to_experiment_name(object_name)

    try:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            if create:
                MlflowClient().create_experiment(name=experiment_name)
                experiment = mlflow.get_experiment_by_name(experiment_name)
            else:
                return True, ""

        return True, dict(experiment)["experiment_id"]
    except:
        crash_report("mlflow.get_id({})".format(object_name))

        return False, ""


def list_registered_models() -> Tuple[
    bool,
    List[str],
]:
    try:
        client = MlflowClient()
        return True, [dict(rm)["name"] for rm in client.list_registered_models()]

    except:
        crash_report("mlflow.list_registered_models()")
        return False, []


def log_artifacts(
    object_name: str,
    path: str,
    model_name: str = "",
) -> bool:
    if not start_run(object_name):
        return False

    try:
        mlflow.log_artifacts(path)

        logger.info("⬆️  {}".format(object_name))

        # https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.register_model
        # https://stackoverflow.com/a/71447758/17619982
        if model_name:
            mv = mlflow.register_model(
                "runs:/{}".format(mlflow.active_run().info.run_id),
                model_name,
                await_registration_for=0,
            )

            logger.info("*️⃣  {} -> {}.{}".format(object_name, mv.name, mv.version))

    except:
        crash_report("mlflow.log_artifacts({},{})".format(object_name, path))
        return False

    return end_run(object_name)


def log_run(
    object_name: str,
    path: str,
) -> bool:
    if not start_run(object_name):
        return False

    for extension in "dot,gif,jpeg,jpg,json,png,sh,xml,yaml".split(","):
        for filename in glob.glob(
            os.path.join(path, f"*.{extension}"),
        ):
            if any(
                [
                    file.size(filename) > 10 * 1024 * 1024,
                    file.name(filename).startswith("thumbnail"),
                ]
            ):
                continue

            mlflow.log_artifact(filename)
            logger.info(f"⬆️  {filename}")

    return end_run(object_name)


# https://www.mlflow.org/docs/latest/search-experiments.html
def search(filter_string: str) -> List[str]:
    client = MlflowClient()

    return [
        to_object_name(experiment.name)
        for experiment in client.search_experiments(
            filter_string=filter_string,
            view_type=ViewType.ALL,
        )
    ]


def set_tags(
    object_name: str,
    tags: Dict[str, str],
    icon="#️⃣ ",
) -> bool:
    experiment_name = to_experiment_name(object_name)

    try:
        tags = Options(tags)

        client = MlflowClient()

        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            client.create_experiment(name=experiment_name)
            experiment = client.get_experiment_by_name(experiment_name)

        for key, value in tags.items():
            client.set_experiment_tag(experiment.experiment_id, key, value)
            logger.info("{} {}.{}={}".format(icon, object_name, key, value))

    except:
        crash_report(f"mlflow.set_tags({object_name})")
        return False

    return True


def start_run(
    object_name: str,
) -> bool:
    run_name = string.pretty_date(
        unique=True,
        include_time=False,
        as_filename=True,
    )

    try:
        mlflow.start_run(
            experiment_id=get_id(object_name, create=True)[1],
            tags=get_tags(object_name)[1],
            run_name=run_name,
        )
        logger.info(f"⏺️  {object_name} | {run_name}")
    except:
        crash_report(f"mlflow.start_run({object_name})")
        return False

    return True


def end_run(
    object_name: str,
) -> bool:
    try:
        mlflow.end_run()
        logger.info("⏹️  {}".format(object_name))
    except:
        crash_report(f"mlflow.end_run({object_name})")
        return False

    return True


def transition(
    model_name: str,
    version: str,
    stage_name: str,
    description: str,
) -> bool:
    logger.info(
        'mlflow.transition({},{},{},"{}")'.format(
            model_name, version, stage_name, description
        )
    )

    try:
        client = MlflowClient()
        client.transition_model_version_stage(
            name=model_name, version=version, stage=stage_name
        )

        if description:
            client.update_model_version(
                name=model_name, version=version, description=description
            )

    except:
        crash_report(
            'mlflow.transition({},{},{},"{}")'.format(
                model_name, version, stage_name, description
            )
        )
        return False

    return True
