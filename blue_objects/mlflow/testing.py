import mlflow

from blue_options import string
from blue_options.logger import crash_report

from blue_objects.mlflow.objects import to_experiment_name
from blue_objects.mlflow.functions import get_id
from blue_objects.logger import logger


def validate() -> bool:
    experiment_name = to_experiment_name(
        string.pretty_date(
            as_filename=True,
            unique=True,
        )
    )

    success, experiment_id = get_id(
        experiment_name,
        create=True,
    )
    if not success:
        return success

    try:
        mlflow.start_run(
            experiment_id=experiment_id,
            tags={"purpose": "validation"},
        )
        mlflow.end_run()

        logger.info("✅ mlflow-{}".format(mlflow.version.VERSION))
    except:
        crash_report("mlflow.validate()")
        return False

    return True
