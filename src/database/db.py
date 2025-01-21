import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('src/database/data.db')
        self.cursor = self.connection.cursor()

        self.__create_tables()

    def close(self) -> None:
        self.connection.close()

    def __create_tables(self) -> None:
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gameVolume INTEGER NOT NULL DEFAULT 100,
                gameWithModifiers BOOLEAN NOT NULL DEFAULT 0
            );

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


class Players(DataBase):
    def __init__(self):
        super().__init__()


class Passing(DataBase):
    def __init__(self):
        super().__init__()

    def add(
            self,
            score: int,
            figures_knocked: int,
            total_bits_thrown: int,
            bonus_level_passed: bool,
            seconds_time_spent: int,
            game_modifiers_ids: str
    ) -> bool:
        self.cursor.execute(
            """
            INSERT INTO passing (score, figuresKnocked, totalBitsThrown, bonusLevelPassed, secondsTimeSpent, gameModifiersIds)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (score, figures_knocked, total_bits_thrown, bonus_level_passed, seconds_time_spent, game_modifiers_ids)
        )
