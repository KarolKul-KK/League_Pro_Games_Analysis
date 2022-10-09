# league_project

# Overview

Project is building to download, store and analyze all League of Legends games in esport. Data was downloaded from website: https://gol.gg
This project was generated using `Kedro 0.18.1`.

# How to install dependencies

```
pip install -r src/requirements.txt
```

# How to download data
1. Install dependencies
2. Run scrapper/urls_scrap.py
3. Run scrapper/main.py

Estimate time: 40 hours


# Pipelines

## data_inserting
```
-db_builder_node: kedro run --node db_builder_node --params param1:<path_to_db>
-general_data_insert_node: kedro run --node general_data_insert_node --params param1:<path_to_file>,param2:<path_to_db> 
-players_stats_insert_node: kedro run --node players_stats_insert_node --params param1:<path_to_file>,param2:<path_to_db>
-team_stats_insert_node: kedro run --node team_stats_insert_node --params param1:<path_to_file>,param2:<path_to_db>
```
