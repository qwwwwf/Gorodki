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
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gameVolume FLOAT NOT NULL DEFAULT 1,
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


class Settings(DataBase):
    def __init__(self):
        super().__init__()
        self.settings_id = 1

    def get(self) -> tuple | None:
        return self.cursor.execute('SELECT * FROM settings WHERE id = ?', (self.settings_id,)).fetchone()

    def get_all(self) -> list:
        return self.cursor.execute('SELECT * FROM settings').fetchall()

    def update_values(self, values: dict):
        sql_query = ', '.join(list(map(lambda x: f'{x} = ?', list(values.keys()))))
        self.cursor.execute(f'UPDATE settings SET {sql_query} WHERE id = ?', tuple(values.values()) + (self.settings_id,))
        self.connection.commit()

    def create(self):
        if not self.get():
            self.cursor.execute('INSERT INTO settings (id) VALUES (?)', (self.settings_id,))
            self.connection.commit()


class Passing(DataBase):
    def __init__(self):
        super().__init__()

    def get(self, game_id: int) -> tuple | None:
        return self.cursor.execute('SELECT * FROM passing WHERE id = ?', (game_id,)).fetchone()

    def get_all(self, sort_id: int = 1) -> list:
        match sort_id:
            case 1:
                add_condition = 'ORDER BY score'
            case 2:
                add_condition = 'ORDER BY totalBitsThrown'
            case 3:
                add_condition = 'ORDER BY figuresKnocked'
            case 4:
                add_condition = 'ORDER BY secondsTimeSpent'
            case _:
                add_condition = ''

        return self.cursor.execute(f'SELECT * FROM passing {add_condition}').fetchall()[::-1]

    def get_best_result(self) -> tuple:
        return self.cursor.execute('SELECT id, score FROM passing ORDER BY -score').fetchone()

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
