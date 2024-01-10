
-- Creating 'weather_data' table
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    weather_text TEXT,
    date TEXT,
    location TEXT
);
