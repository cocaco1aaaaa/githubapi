CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    repo VARCHAR(255),
    owner VARCHAR(255),
    position_cur INTEGER,
    position_prev INTEGER,
    stars INTEGER,
    watchers INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    language VARCHAR(50)
);

CREATE TABLE repo_activity (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repos(id),
    date DATE,
    commits INTEGER,
    authors TEXT[]
);
