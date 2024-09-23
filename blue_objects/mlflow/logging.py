import os
import glob
import mlflow

from blueness import module

from blue_objects import file, NAME
from blue_options.logger import crash_report
from blue_objects.mlflow.runs import start_run, end_run
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


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
        crash_report(f"{NAME}.log_artifacts({object_name}): {path}")
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
