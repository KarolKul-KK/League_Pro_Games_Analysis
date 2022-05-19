"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from .pipelines import data_inserting


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_inserting_pipeline = data_inserting.create_pipeline()
    return {"__default__": data_inserting_pipeline,
            "data_inserting": data_inserting_pipeline,
    }
