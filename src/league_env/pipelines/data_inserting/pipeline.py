import argparse
from kedro.framework.context.context import KedroContext
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import skipping_bad_lines, inserting_general_data, inserting_players_stats, inserting_team_stats


param_key1 = KedroContext.params()
param_key2 = KedroContext.params()


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=skipping_bad_lines,
                inputs=param_key1,
                outputs=None,
                name="skipping_bad_lines_node",
            ),
            node(
                func=inserting_general_data,
                inputs=[param_key1, param_key2],
                outputs=None,
                name="general_data_insert_node"
            ),
            node(
                func=inserting_players_stats,
                inputs=[param_key1, param_key2],
                outputs=None,
                name="players_stats_insert_node"
            ),
            node(
                func=inserting_team_stats,
                inputs=[param_key1, param_key2],
                outputs=None,
                name="team_stats_insert_node"
            )
        ]
    )



