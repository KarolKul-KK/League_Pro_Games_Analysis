import sqlite3
import os


path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
conn = sqlite3.connect(os.path.join(path, "LEAGUE_PRO_GAMES_ANALYSIS/data", "league.db"))
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
