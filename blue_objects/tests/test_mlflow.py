from blue_objects.objects import unique_object
from blue_objects.mlflow.objects import from_experiment_name, to_experiment_name


def test_from_and_to_experiment_name():
    object_name = unique_object()

    assert from_experiment_name(to_experiment_name(object_name)) == object_name
