DROP TABLE IF EXISTS groups;
    CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);


    DROP TABLE IF EXISTS teachers;
    CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    fullname TEXT
);

    DROP TABLE IF EXISTS students;
    CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    fullname TEXT,
    group_id INTEGER REFERENCES groups (id)
);

    DROP TABLE IF EXISTS disciplines;
    CREATE TABLE disciplines (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    teacher_id INTEGER REFERENCES teachers (id)
);

    DROP TABLE IF EXISTS grades;
    CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students (id),
    discipline_id INTEGER REFERENCES disciplines (id),
    grade INTEGER,
    date_of DATE
);