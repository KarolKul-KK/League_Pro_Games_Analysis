# league_project

## Overview

Project is building to download, store and analyze all League of Legends games in esport. Data is download from website: https://www.op.gg
This project was generated using `Kedro 0.18.1`.

## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
pip install -r src/requirements.txt
```

## How to download data
1. Install dependencies
2. Run urls_scrap.py
3. Run main.py

Estimate time: 40 hours


## Pipelines

# data_inserting

-db_builder_node: kedro run --node db_builder_node --params param1:<path_to_db>
-general_data_insert_node: kedro run --node general_data_insert_node --params param1:<path_to_file>,param2:<path_to_db> 
-players_stats_insert_node: kedro run --node general_data_insert_node --params param1:<path_to_file>,param2:<path_to_db>
-team_stats_insert_node: kedro run --node general_data_insert_node --params param1:<path_to_file>,param2:<path_to_db>
