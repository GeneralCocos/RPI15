CREATE TABLE IF NOT EXISTS subject (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    day TEXT NOT NULL,
    room_numb TEXT NOT NULL,
    start_time TEXT NOT NULL,
    FOREIGN KEY (subject_name) REFERENCES subject(name)
);