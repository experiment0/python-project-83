DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    -- http://www.postgresql.org/docs/8.1/static/sql-createtable.html#SQL-CREATETABLE-NOTES
    -- PostgreSQL automatically creates an index for each unique constraint and primary key constraint to enforce uniqueness.
    -- PostgreSQL автоматически создает индекс для каждого уникального ограничения и ограничения первичного ключа для обеспечения уникальности.
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY, 
    url_id INTEGER NOT NULL, 
    status_code SMALLINT NOT NULL, 
    h1 VARCHAR(255), 
    title VARCHAR(255), 
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (url_id) REFERENCES urls (id)
);