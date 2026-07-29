-- PostgreSQL Database Initialization Script

-- 1. Create the 'tasks' table if it does not exist
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    user_id TEXT
);

-- 2. Create index on user_id for multi-tenant query performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- 3. Seed initial 3 tasks
INSERT INTO tasks (title, done, user_id)
VALUES 
    ('Buy groceries', FALSE, NULL),
    ('Read PostgreSQL documentation', FALSE, NULL),
    ('Build FastAPI application with PostgreSQL', TRUE, NULL);

