from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score
from typing import Tuple
import pandas as pd
import sqlite3
from sqlite3 import Error
import os


path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))


def create_connection(db_file: str) -> sqlite3.Connection:

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_data_to_ml_model(conn: sqlite3.Connection) -> list:
    cur = conn.cursor()
    cur.execute(
        """SELECT           Result,
                            Kills,
                            First_Blood,
                            First_Tower,
                            Dragons,
                            Barons, 
                            Gold, 
                            Ban_1,
                            Team_stats.Match_id,
                            General_Data.Time
                    FROM Team_Stats
                    INNER JOIN General_Data
                    ON Team_Stats.Match_id = General_Data.Match_id
                    """
    )

    rows = cur.fetchall()
    return rows


def one_hot_encoder(df: pd.DataFrame) -> pd.DataFrame:
    enc = OneHotEncoder(handle_unknown="ignore")
    encoder_df = pd.DataFrame(enc.fit_transform(df[["Ban_1"]]).toarray())
    df_final = df.join(encoder_df)
    df_final.dropna(inplace=True)

    return df_final


def split_data(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    y = df["Result"]
    df.drop(["Ban_1", "Result", "Match_id"], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(
        df, y, test_size=0.20, random_state=42
    )

    return X_train, X_test, y_train, y_test


def fit_dummy_classifier(
    X_train: pd.DataFrame, X_test: pd.Series, y_train: pd.DataFrame, y_test: pd.Series
) -> Tuple[float, float]:
    dummy_class = DummyClassifier()
    dummy_class.fit(X_train, y_train)
    dummy_score = dummy_class.score(X_test, y_test)
    dummy_pred = dummy_class.predict(X_test)
    b_accuracy = balanced_accuracy_score(y_test, dummy_pred)

    return dummy_score, b_accuracy


def fit_clf_classifier(
    X_train: pd.DataFrame, X_test: pd.Series, y_train: pd.DataFrame, y_test: pd.Series
) -> Tuple[float, float]:
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    clf_score = clf.score(X_test, y_test)
    clf_pred = clf.predict(X_test)
    b_accuracy = balanced_accuracy_score(y_test, clf_pred)

    return clf_score, b_accuracy


if __name__ == "__main__":
    conn = create_connection(os.path.join(path, "data/league.db"))
    columns_names = [
        "Result",
        "Kills",
        "First_Blood",
        "First_Tower",
        "Dragons",
        "Barons",
        "Gold",
        "Ban_1",
        "Match_id",
        "Time",
    ]
    data = select_data_to_ml_model(conn)

    df_general = pd.DataFrame(data, columns=columns_names)
    df_general["Result"] = df_general["Result"].apply(lambda x: 1 if x == "WIN" else 0)
    df_general["Time"] = df_general["Time"].apply(lambda x: float(x.replace(":", ".")))
    df_general["Gold"] = df_general["Gold"].apply(
        lambda x: float(x.replace("k", "000").replace(".", ""))
    )
    df_general["First_Blood"] = df_general["First_Blood"].apply(lambda x: float(x))
    final_df = one_hot_encoder(df_general)

    X_train, X_test, y_train, y_test = split_data(final_df)

    dummy_score, mse_dummy = fit_dummy_classifier(X_train, X_test, y_train, y_test)
    knc_score, mse_knc = fit_clf_classifier(X_train, X_test, y_train, y_test)

    print(f"Dummy classifier: {dummy_score} score and {mse_dummy} balanced accuracy")
    print(f"CLF classifier: {knc_score} score and {mse_knc} balanced accuracy")
