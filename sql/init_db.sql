-- Init DB for Prätkä-parkit

PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parking_spot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    title TEXT,
    description TEXT,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    address TEXT,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE classifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE item_classifications (
    item_id INTEGER NOT NULL,
    classification_id INTEGER NOT NULL,
    PRIMARY KEY (item_id, classification_id),
    FOREIGN KEY(item_id) REFERENCES parking_spot(id) ON DELETE CASCADE,
    FOREIGN KEY(classification_id) REFERENCES classifications(id) ON DELETE CASCADE
);

INSERT INTO classifications (name) VALUES
    ('Asfaltti'),
    ('Sorapinta'),
    ('Maksuton'),
    ('Maksullinen'),
    ('Katettu'),
    ('Lämmitetty');

CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_spot_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(parking_spot_id) REFERENCES parking_spot(id) ON DELETE CASCADE,
    FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE CASCADE
);
