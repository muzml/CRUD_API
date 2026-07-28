-- PostgreSQL Database Initialization Script

-- 1. Create the 'tasks' table if it does not exist
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

-- 2. Seed initial 3 tasks
INSERT INTO tasks (title, done)
VALUES 
    ('Buy groceries', FALSE),
    ('Read PostgreSQL documentation', FALSE),
    ('Build FastAPI application with PostgreSQL', TRUE);
