from kedro.pipeline import Pipeline, node, pipeline
from .nodes import db_builder, inserting_general_data, inserting_players_stats, inserting_team_stats


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=db_builder,
                inputs="params:param1",
                outputs=None,
                name="db_builder_node",
            ),
            node(
                func=inserting_general_data,
                inputs=['params:param1', 'params:param2'],
                outputs=None,
                name="general_data_insert_node"
            ),
            node(
                func=inserting_players_stats,
                inputs=['params:param1', 'params:param2'],
                outputs=None,
                name="players_stats_insert_node"
            ),
            node(
                func=inserting_team_stats,
                inputs=['params:param1', 'params:param2'],
                outputs=None,
                name="team_stats_insert_node"
            )
        ]
    )



