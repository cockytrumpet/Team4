CREATE TABLE IF NOT EXISTS tags (
    id serial PRIMARY KEY,
    title varchar (150) NOT NULL,
    descr text
    );
INSERT INTO tags (title, descr) VALUES 
    ('tag1','descr');

CREATE TABLE IF NOT EXISTS resources (
    id serial PRIMARY KEY,
    create_date DATE DEFAULT (CURRENT_DATE),
    title varchar (150) NOT NULL,
    link text,
    descr text
    );

INSERT INTO resources (title, link, descr) VALUES 
    ('Stack Overflow Article',
    'https://stackoverflow.com/questions/20461030/current-date-curdate-not-working-as-default-date-value',
    'Current Date Function'
    );
