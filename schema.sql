CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE tasks(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    priority INTEGER,
    deadline TIMESTAMP
);

CREATE TABLE events(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);
