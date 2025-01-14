import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('src/database/data.db')
        self.cursor = self.connection.cursor()

        self.__create_tables()

    def close_db(self) -> None:
        self.connection.close()

    def __create_tables(self) -> None:
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS passing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL DEFAULT 0,
                figuresKnocked INTEGER NOT NULL DEFAULT 0,
                totalBitsThrown INTEGER NOT NULL DEFAULT 0,
                bonusLevelPassed BOOLEAN NOT NULL DEFAULT 0,
                secondsTimeSpent INTEGER NOT NULL DEFAULT 0,
                gameModifiersId VARCHAR(50),
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
