import argparse
from functools import reduce
import os

from blueness.argparse.generic import sys_exit
from blueness import module

from blue_objects import NAME
from blue_objects.mlflow.functions import (
    delete,
    get_id,
    get_tags,
    list_registered_models,
    log_artifacts,
    log_run,
    search,
    set_tags,
    transition,
    validate,
)
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    default="",
    help="clone_tags|delete|get_tags|get_id|list_registered_models|log_artifacts|log_run|search|set_tags|transition|validate",
)
parser.add_argument(
    "--count",
    type=int,
    default=-1,
)
parser.add_argument(
    "--default",
    type=str,
    default="",
)
parser.add_argument(
    "--delim",
    type=str,
    default=",",
)
parser.add_argument(
    "--description",
    type=str,
    default="",
)
parser.add_argument(
    "--destination_experiment",
    type=str,
    default="",
)
parser.add_argument(
    "--experiment_name",
    type=str,
    default=os.getenv("abcli_object_name"),
)
parser.add_argument(
    "--filter_string",
    type=str,
    help="tags.`keyword` = `value` - https://www.mlflow.org/docs/latest/search-runs.html",
)
parser.add_argument(
    "--input",
    type=str,
    default="name",
    help="id|name",
)
parser.add_argument(
    "--item_name_plural",
    type=str,
    default="experiment(s)",
)
parser.add_argument(
    "--model_name",
    type=str,
    default="",
)
parser.add_argument(
    "--output",
    type=str,
    default="name",
    help="id|name",
)
parser.add_argument(
    "--path",
    type=str,
    default="",
)
parser.add_argument(
    "--regex",
    type=str,
    default="",
)
parser.add_argument(
    "--show_count",
    type=int,
    default=1,
    help="0|1",
)
parser.add_argument(
    "--start_end",
    type=str,
    default="",
    help="start|end",
)
parser.add_argument(
    "--stage_name",
    type=str,
    default="",
    help="",
)
parser.add_argument(
    "--tag",
    type=str,
    default="",
)
parser.add_argument(
    "--source_experiment",
    type=str,
    default="",
)
parser.add_argument(
    "--tags",
    type=str,
    default="",
    help="+this,that=which,what=12",
)
parser.add_argument(
    "--value",
    type=str,
    default="",
)
parser.add_argument(
    "--version",
    type=str,
    default="",
    help="",
)
args = parser.parse_args()

delim = ", " if args.show_count else " " if args.delim == "space" else args.delim

success = False
if args.task == "clone_tags":
    success, tags = get_tags(args.source_experiment)
    if success:
        success = set_tags(args.destination_experiment, tags)
elif args.task == "delete":
    success = reduce(
        lambda x, y: x and y,
        [
            delete(experiment_name, is_id=args.input == "id")
            for experiment_name in args.experiment_name.split(",")
            if experiment_name
        ],
        True,
    )
elif args.task == "get_tags":
    success, tags = get_tags(args.experiment_name)
    print(tags if not args.tag else tags.get(args.tag, args.default))
elif args.task == "get_id":
    success, id = get_id(args.experiment_name)
    print(id)
elif args.task == "list_registered_models":
    success, list_of_models = list_registered_models()
    if args.show_count:
        logger.info(
            "{:,} model(s): {}".format(len(list_of_models), delim.join(list_of_models))
        )
    else:
        print(delim.join(list_of_models))
elif args.task == "log_artifacts":
    success = log_artifacts(args.experiment_name, args.path, args.model_name)
elif args.task == "log_run":
    success = log_run(args.experiment_name, args.path)
elif args.task == "search":
    success = True
    experiment_name_list = search(args.filter_string)

    if args.show_count:
        logger.info(
            "{:,} {}: {}".format(
                len(experiment_name_list),
                args.item_name_plural,
                delim.join(experiment_name_list),
            )
        )
    else:
        print(delim.join(experiment_name_list))
elif args.task == "set_tags":
    success = set_tags(args.experiment_name, args.tags)
elif args.task == "transition":
    success = transition(
        args.model_name, args.version, args.stage_name, description=args.description
    )
elif args.task == "validate":
    success = validate()
else:
    success = None

sys_exit(logger, NAME, args.task, success)
