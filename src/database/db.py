import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('src/database/data.db')
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def create_tables(self) -> None:
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


class Player(DataBase):
    def __init__(self):
        super().__init__()

    def get(self, player_id: int) -> tuple | None:
        return self.cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()

    def get_all(self) -> list:
        return self.cursor.execute('SELECT * FROM players').fetchall()

    def update_values(self, values: dict):
        # TODO: доделать
        self.cursor.execute('')
        self.connection.commit()

    def create(self):
        if not self.get(1):
            self.cursor.execute('INSERT INTO players (id) VALUES (?)', (1,))
            self.connection.commit()


class Passing(DataBase):
    def __init__(self):
        super().__init__()

    def get_all(self) -> list:
        return self.cursor.execute('SELECT * FROM passing').fetchall()[::-1]

    def add(
            self,
            score: int,
            figures_knocked: int,
            total_bits_thrown: int,
            bonus_level_passed: bool,
            seconds_time_spent: int,
            game_modifiers_ids: str
    ):
        self.cursor.execute(
            """
            INSERT INTO passing (score, figuresKnocked, totalBitsThrown, bonusLevelPassed, secondsTimeSpent, gameModifiersId)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (score, figures_knocked, total_bits_thrown, bonus_level_passed, seconds_time_spent, game_modifiers_ids)
        ).fetchone()
        self.connection.commit()
