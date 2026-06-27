DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

INSERT INTO students (name, age, course, email)
VALUES
('Mukul',20,'BCA','mukul@example.com'),
('Rahul',21,'B.Tech','rahul@example.com'),
('Priya',19,'BCA','priya@example.com');