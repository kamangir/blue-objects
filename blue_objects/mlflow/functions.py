from typing import Tuple, Dict, List
import copy
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import re

from blue_options import string
from blue_options.options import Options
from blue_options.logger import crash_report

from blue_objects.logger import logger


def delete(
    experiment_name: str,
    is_id: bool = False,
) -> bool:
    if is_id:
        experiment_id = experiment_name
    else:
        success, experiment_id = get_id(experiment_name)
        if not success:
            return success

    try:
        client = MlflowClient()

        # get list of run_ids

        # delete all runs

        client.delete_experiment(experiment_id)
    except:
        crash_report("mlflow.delete({})".format(experiment_name))
        return False

    logger.info(
        "🚮 {}".format(
            "#{}".format(experiment_id)
            if is_id
            else "{} (#{})".format(experiment_name, experiment_id)
        )
    )

    return True


def get_tags(
    experiment_name: str,
) -> Tuple[bool, Dict[str, str]]:
    try:
        client = MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)

        if experiment is None:
            return True, {}

        return True, copy.deepcopy(experiment.tags)
    except:
        crash_report("mlflow.get_tags({})".format(experiment_name))
        return False, {}


def get_id(
    experiment_name: str,
    create: bool = False,
) -> Tuple[bool, str]:
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
        crash_report("mlflow.get_id({})".format(experiment_name))

        return False, ""


def list_(
    count: int = -1,
    return_id: bool = False,
    regex: str = "",
) -> Tuple[bool, List[str]]:
    try:
        client = MlflowClient()

        output = [
            exp.experiment_id if return_id else exp.name
            for exp in client.list_experiments()
        ]

        if regex:
            output = [thing for thing in output if re.search(regex, thing) is not None]

        if count != -1:
            output = output[:count]

    except:
        crash_report("mlflow.list()")
        return False, []

    return True, output


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
    experiment_name: str,
    path: str,
    model_name: str = "",
) -> bool:
    success = start_end_run(experiment_name, start=True)

    if success:
        try:
            mlflow.log_artifacts(path)

            logger.info("⬆️  {}".format(experiment_name))

            # https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.register_model
            # https://stackoverflow.com/a/71447758/17619982
            if model_name:
                mv = mlflow.register_model(
                    "runs:/{}".format(mlflow.active_run().info.run_id),
                    model_name,
                    await_registration_for=0,
                )

                logger.info(
                    "*️⃣  {} -> {}.{}".format(experiment_name, mv.name, mv.version)
                )

        except:
            crash_report("mlflow.log_artifacts({},{})".format(experiment_name, path))
            success = False

    if success:
        success = start_end_run(experiment_name, end=True)

    return success


def log_run(
    experiment_name: str,
    path: str,
) -> bool:
    success = start_end_run(experiment_name, start=True)

    if success:
        success = start_end_run(experiment_name, end=True)

    return success


# https://www.mlflow.org/docs/latest/search-runs.html
def search(filter_string: str) -> Tuple[
    bool,
    List[str],
]:
    logger.info("🔍 {}".format(filter_string))

    client = MlflowClient()

    all_experiments = [exp.experiment_id for exp in client.list_experiments()]

    runs = client.search_runs(
        experiment_ids=all_experiments,
        filter_string=filter_string,
        run_view_type=ViewType.ALL,
    )

    return True, [
        client.get_experiment(exp_id).name
        for exp_id in {run.info.experiment_id for run in runs}
    ]


def set_tags(
    experiment_name: str,
    tags: Dict[str, str],
    icon="#️⃣ ",
) -> bool:
    try:
        tags = Options(tags)

        client = MlflowClient()

        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            client.create_experiment(name=experiment_name)
            experiment = client.get_experiment_by_name(experiment_name)

        for key, value in tags.items():
            client.set_experiment_tag(experiment.experiment_id, key, value)
            logger.info("{} {}.{}={}".format(icon, experiment_name, key, value))

    except:
        crash_report("mlflow.set_tags()")
        return False

    return True


def start_end_run(
    experiment_name: str,
    end: bool = False,
    start: bool = False,
) -> bool:
    try:
        if end:
            mlflow.end_run()
            logger.info("⏹️  {}".format(experiment_name))
        elif start:
            mlflow.start_run(
                experiment_id=get_id(experiment_name, create=True)[1],
                tags=get_tags(experiment_name)[1],
            )
            logger.info("⏺️  {}".format(experiment_name))
        else:
            logger.error("mlflow.start_end_run(): bad start/stop.")

        return True
    except:
        crash_report(
            "mlflow.start_end_run({},{},{})".format(experiment_name, start, end)
        )
        return False


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


def validate() -> bool:
    experiment_name = string.pretty_date(
        as_filename=True,
        unique=True,
    )

    try:
        mlflow.start_run(
            experiment_id=get_id(experiment_name, create=True)[1],
            tags={"purpose": "validation"},
        )
        mlflow.end_run()

        logger.info("✅ mlflow-{}".format(mlflow.version.VERSION))
    except:
        crash_report("mlflow.validate()")
        return False

    return True
