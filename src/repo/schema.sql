CREATE TABLE user_roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL
);
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    user_role INTEGER NOT NULL,
    FOREIGN KEY (user_role) REFERENCES user_roles (role_id)
);
CREATE TABLE operations (
    operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT NOT NULL,
    amount REAL NOT NULL,
    descriprion TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
INSERT INTO user_roles (role_name) VALUES ('Руководитель', 'Бухгалтер');
INSERT INTO users (login, password, user_role) VALUES ('admin', 'admin1', 1);