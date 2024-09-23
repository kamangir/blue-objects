from typing import Tuple, List
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

from blueness import module
from blue_options import string
from blue_options.logger import crash_report

from blue_objects import NAME
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


def end_run(
    object_name: str,
) -> bool:
    try:
        mlflow.end_run()
        logger.info("⏹️  {}".format(object_name))
    except:
        crash_report(f"{NAME}.end_run({object_name})")
        return False

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
        crash_report(f"{NAME}.get_run_id({object_name})")
        return False, []


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
