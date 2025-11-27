import sqlite3


class FlightDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("flights.sqlite")
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys = ON")

    def create_nationalities_table(self):
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS nationalities(
            id INTEGER Primary Key Autoincrement,
            name TEXT UNIQUE NOT NULL
            )"""
        )

    def create_iata_codes_table(self):
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS iata_codes(
            id INTEGER Primary Key Autoincrement,
            code TEXT UNIQUE NOT NULL
            )"""
        )
        pass

    def create_users_table(self):
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id INTEGER Primary Key Autoincrement,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            nationality_id INTEGER NOT NULL REFERENCES nationalities(id),
            date_of_birth TEXT NOT NULL,
            passport_number TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'passenger',
            created_at TEXT DEFAULT CURRENT_DATE
            )"""
        )

    def create_airlines_table(self):
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS airlines(
            id INTEGER Primary Key Autoincrement,
            name TEXT UNIQUE NOT NULL,
            iata_code TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            country,
            headquarters,
            fleet_size,
            founder_year,
            )"""
        )
        # countries table

    def create_airports_table(self):
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS airports(
            id,
            name,
            iata_code,
            city,
            country,
            timezone, ?
            latitude, ?
            longtitude, ?
            elevation, ?
            )"""
        )
        # countries table
        # timezone? може да се извлече от държава + град
        # latitude & longtitude?
        # elevation?


db = FlightDatabase()
db.create_nationalities_table()
db.create_users_table()


# db.curs.execute(
#     """ INSERT INTO users (
#     email,
#     password,
#     first_name,
#     last_name,
#     phone_number,
#     nationality,
#     date_of_birth,
#     passport_number
# ) VALUES (
#     'jane.smith@example.com',
#     'mypassword456',
#     'Jane',
#     'Smith',
#     '+1987654321',
#     'UK',
#     '1992-08-20',
#     'B98765432'
# );
#  """
# )
# db.conn.commit()
# db.curs.execute("Select * from users")
# print(db.curs.fetchone())
