-- Converted by mysql_dump_to_sqlite
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers (
customer_id INTEGER NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
email TEXT,
phone TEXT
);
DELETE FROM customers;
INSERT INTO customers (customer_id, first_name, last_name, email, phone) VALUES
(1, 'Paolo', 'Ferrari', 'paolo.ferrari@email.it', '3331112223'),
(2, 'Anna', 'Conti', 'anna.conti@email.it', '3342223334'),
(3, 'Lorenzo', 'Martini', 'lorenzo.martini@email.it', '3353334445'),
(4, 'Sara', 'Greco', 'sara.greco@email.it', '3364445556'),
(5, 'Davide', 'Colombo', 'davide.colombo@email.it', '3375556667'),
(6, 'Valentina', 'Ricci', 'valentina.ricci@email.it', '3386667778'),
(7, 'Simone', 'Esposito', 'simone.esposito@email.it', '3397778889'),
(8, 'Roberta', 'Gatti', 'roberta.gatti@email.it', '3408889990'),
(9, 'Matteo', 'Lombardi', 'matteo.lombardi@email.it', '3419990001'),
(10, 'Federica', 'Barbieri', 'federica.barbieri@email.it', '3420001112');
DROP TABLE IF EXISTS departments;
CREATE TABLE IF NOT EXISTS departments (
department_id INTEGER NOT NULL,
department_name TEXT NOT NULL
);
DELETE FROM departments;
INSERT INTO departments (department_id, department_name) VALUES
(1, 'Amministrazione'),
(2, 'Vendite'),
(3, 'Marketing'),
(4, 'IT'),
(5, 'Produzione');
DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS employees (
employee_id INTEGER NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
email TEXT,
hire_date TEXT,
salary REAL DEFAULT NULL,
department_id INTEGER DEFAULT NULL
);
DELETE FROM employees;
INSERT INTO employees (employee_id, first_name, last_name, email, hire_date, salary, department_id) VALUES
(1, 'Luca', 'Bianchi', 'luca.bianchi@azienda.it', '2020-01-15', 28000, 2),
(2, 'Maria', 'Rossi', 'maria.rossi@azienda.it', '2019-03-10', 30000, 3),
(3, 'Giovanni', 'Verdi', 'giovanni.verdi@azienda.it', '2021-07-01', 27000, 4),
(4, 'Chiara', 'Neri', 'chiara.neri@azienda.it', '2018-05-20', 32000, 1),
(5, 'Marco', 'Russo', 'marco.russo@azienda.it', '2022-02-14', 25000, 5),
(6, 'Francesca', 'Gallo', 'francesca.gallo@azienda.it', '2020-08-05', 29500, 2),
(7, 'Alessandro', 'Costa', 'alessandro.costa@azienda.it', '2017-11-30', 33000, 3),
(8, 'Giulia', 'Fontana', 'giulia.fontana@azienda.it', '2019-09-18', 31000, 4),
(9, 'Stefano', 'Moretti', 'stefano.moretti@azienda.it', '2021-04-22', 26500, 5),
(10, 'Elena', 'Rinaldi', 'elena.rinaldi@azienda.it', '2020-12-12', 28500, 1);
DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products (
product_id INTEGER NOT NULL,
product_name TEXT NOT NULL,
price REAL DEFAULT NULL,
stock INTEGER DEFAULT NULL
);
DELETE FROM products;
INSERT INTO products (product_id, product_name, price, stock) VALUES
(1, 'Tavolo in legno', 150, 10),
(2, 'Sedia da ufficio', 80, 25),
(3, 'Lampada da tavolo', 45, 40),
(4, 'Notebook 15"', 700, 8),
(5, 'Stampante laser', 120, 15),
(6, 'Mouse wireless', 20, 50),
(7, 'Tastiera meccanica', 60, 30),
(8, 'Monitor 24"', 180, 12),
(9, 'Zaino porta PC', 35, 20),
(10, 'Cuffie bluetooth', 55, 18);
DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders (
order_id INTEGER NOT NULL,
customer_id INTEGER DEFAULT NULL,
order_date TEXT,
status TEXT
);
DELETE FROM orders;
INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
(1, 1, '2023-06-15', 'spedito'),
(2, 2, '2023-06-18', 'in lavorazione'),
(3, 3, '2023-07-01', 'spedito'),
(4, 4, '2023-07-05', 'spedito'),
(5, 5, '2023-07-10', 'annullato'),
(6, 6, '2023-07-12', 'spedito'),
(7, 7, '2023-07-15', 'in lavorazione'),
(8, 8, '2023-07-18', 'spedito'),
(9, 9, '2023-07-20', 'spedito'),
(10, 10, '2023-07-22', 'spedito');
DROP TABLE IF EXISTS order_items;
CREATE TABLE IF NOT EXISTS order_items (
order_item_id INTEGER NOT NULL,
order_id INTEGER DEFAULT NULL,
product_id INTEGER DEFAULT NULL,
quantity INTEGER DEFAULT NULL
);
DELETE FROM order_items;
INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES
(1, 1, 1, 1),
(2, 1, 6, 2),
(3, 2, 3, 1),
(4, 3, 4, 1),
(5, 3, 5, 1),
(6, 4, 2, 4),
(7, 5, 7, 2),
(8, 6, 8, 1),
(9, 7, 9, 3),
(10, 8, 10, 1),
(11, 9, 1, 1),
(12, 9, 2, 2),
(13, 10, 6, 1),
(14, 10, 3, 2);
PRAGMA foreign_keys = ON;
