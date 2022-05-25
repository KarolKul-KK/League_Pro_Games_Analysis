import pandas as pd
import sqlite3
from sqlite3 import Error
from kedro.pipeline import node


def _create_connection(db_file: str) -> sqlite3.Connection:

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def _general_data_insert(conn: sqlite3.Connection, general_data: pd.DataFrame) -> None:

    sql = ''' INSERT INTO General_Data(
              Match_id,
              Date, 
              Blue_Team, 
              Red_Team, 
              Tournament, 
              Time, 
              Game_Version)
              VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, general_data)
    conn.commit()


def _players_stats_insert(conn: sqlite3.Connection, players_data: pd.DataFrame) -> None:

    sql = ''' INSERT INTO Players_Stats(
              Player_Nickname,
              KDA,
              CS,
              Damage_Distribution,
              Gold_Distribution,
              Champion,
              Role,
              Match_id,
              Match_count)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, players_data)
    conn.commit()


def _team_stats_insert(conn: sqlite3.Connection, teams_data: pd.DataFrame) -> None:

    sql =  """
            Insert into Team_Stats(
              Club_Name,
              Result,
              Kills,
              First_Blood,
              Towers,
              First_Tower,
              Dragons,
              Barons,
              Gold,
              Ban_1,
              Ban_2,
              Ban_3,
              Ban_4,
              Ban_5,
              Pick_1,
              Pick_2,
              Pick_3,
              Pick_4,
              Pick_5,
              match_id,
              match_count
            )   
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          """
    cur = conn.cursor()
    cur.execute(sql, teams_data)
    conn.commit()


def _string_to_list(string: str) -> list:
    return string.replace('[', '').replace(']', '').replace("'", '').split(',')


def inserting_general_data(csv_file_path: str, db_file: str) -> None:

    conn = _create_connection(db_file)
    df_general = pd.read_csv(csv_file_path, index_col=0)
    for i in range(len(df_general)):
        _general_data_insert(conn, df_general.iloc[i])


def inserting_players_stats(csv_file_path: str, db_file: str) -> None:

    conn = _create_connection(db_file)
    df_players_stats = pd.read_csv(csv_file_path, index_col=0)
    for i in range(len(df_players_stats)):
        _players_stats_insert(conn, df_players_stats.iloc[i])


def inserting_team_stats(csv_file_path: str, db_file: str) -> None:

    conn = _create_connection(db_file)
    df = pd.read_csv(csv_file_path, index_col=0)
    for i in range(len(df)):
        bans = _string_to_list(df['Bans'][i])
        picks = _string_to_list(df['Picks'][i])
        _team_stats_insert(conn, [df['Name'][i], df['Result'][i], df['Kills'][i], df['First_Blood'][i], df['Towers'][i],
       df['First_Tower'][i], df['Dragons'][i], df['Barons'][i], df['Gold'][i], bans[0], bans[1], bans[2], bans[3], bans[4], picks[0], picks[1], picks[2], picks[3], picks[4], df['Match_id'][i],
       df['Match_count'][i]])



def db_builder(db_file_path: str) -> None:
    
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()

    c.execute(
        """
            CREATE TABLE IF NOT EXISTS General_Data(
                Match_id INTEGER,
                Date  TIMESTAMP,
                Blue_Team TEXT,
                Red_Team TEXT,
                Tournament TEXT,
                Time TEXT,
                Game_Version TEXT
                )
            """
    )

    c.execute(
        """
            CREATE TABLE IF NOT EXISTS Players_Stats(
                Player_Nickname TEXT,
                KDA TEXT,
                CS INTEGER,
                Damage_Distribution TEXT,
                Gold_Distribution TEXT,
                Champion TEXT,
                Role TEXT,
                Match_id INTEGER,
                Match_count INTEGER
                )   
            """
    )

    c.execute(
        """
            CREATE TABLE IF NOT EXISTS Team_Stats(
                Club_Name TEXT,
                Result TEXT,
                Kills INTEGER,
                First_Blood TEXT,
                Towers INTEGER,
                First_Tower INTEGER,
                Dragons INTEGER,
                Barons INTEGER,
                Gold TEXT,
                Ban_1 TEXT,
                Ban_2 TEXT,
                Ban_3 TEXT,
                Ban_4 TEXT,
                Ban_5 TEXT,
                Pick_1 TEXT,
                Pick_2 TEXT,
                Pick_3 TEXT,
                Pick_4 TEXT,
                Pick_5 TEXT,
                match_id INTEGER,
                match_count INTEGER
                )   
            """
    )

    conn.commit()


def skipping_bad_lines(csv_file_path: str) -> None:
    '''Function read csv, skipping bad lines and save csv'''
    df = pd.read_csv(csv_file_path, index_col=0, error_bad_lines=False)
    df.to_csv(csv_file_path)