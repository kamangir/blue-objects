# 🌀 blue-objects

🌀 `blue-objects` are the inputs and outputs of [AI algo](https://github.com/kamangir/giza). They are maintained in [AWS S3](https://aws.amazon.com/s3/) and their metadata is tracked by [MLflow](https://mlflow.org/).

For example, the Sentinel-2 [datacube](https://github.com/kamangir/blue-geo/tree/main/blue_geo/datacube) `datacube-EarthSearch-sentinel_2_l1c-S2A_10UDC_20240731_0_L1C` and 🌐 [`@geo watch` outputs](https://github.com/kamangir/blue-geo/tree/main/blue_geo/watch) are `blue-objects`.

```bash
pip install blue-objects
```

---

to use on [AWS SageMaker](https://aws.amazon.com/sagemaker/) replace `<plugin-name>` with "blue_objects" and follow [these instructions](https://github.com/kamangir/notebooks-and-scripts/blob/main/SageMaker.md).

[![pylint](https://github.com/kamangir/blue-objects/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/blue-objects/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/blue-objects/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/blue-objects.svg)](https://pypi.org/project/blue-objects/)

built by 🌀 [`blue_options-4.97.1`](https://github.com/kamangir/awesome-bash-cli), based on 🌀 [`blue_objects-5.127.1`](https://github.com/kamangir/blue-objects).

