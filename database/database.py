import sqlite3

from pathlib import Path

from datetime import datetime


DATABASE_PATH = Path(__file__).parent / "soteria.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            module TEXT NOT NULL,

            score INTEGER,

            verdict TEXT,

            summary TEXT,

            filename TEXT,

            timestamp TEXT

        )

    """)

    connection.commit()

    connection.close()


def save_history(

    module,

    score,

    verdict,

    summary,

    filename=None

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        INSERT INTO history (

            module,

            score,

            verdict,

            summary,

            filename,

            timestamp

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

            module,

            score,

            verdict,

            summary,

            filename,

            datetime.now().strftime(

                "%d %b %Y • %I:%M %p"

            )

        )

    )

    connection.commit()

    connection.close()


def get_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        SELECT *

        FROM history

        ORDER BY id DESC

        """

    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def clear_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM history"

    )

    connection.commit()

    connection.close()