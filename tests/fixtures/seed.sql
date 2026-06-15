-- Demo retail dataset for the offline test suite (deterministic, fixed dates).
CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    name      TEXT NOT NULL
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL
);
CREATE TABLE sales (
    sale_id    INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    branch_id  INTEGER NOT NULL,
    sale_date  TEXT    NOT NULL,
    qty        INTEGER NOT NULL,
    revenue    REAL    NOT NULL
);
CREATE TABLE inventory (
    product_id INTEGER NOT NULL,
    branch_id  INTEGER NOT NULL,
    on_hand    INTEGER NOT NULL
);

INSERT INTO branches (branch_id, name) VALUES (1, 'Downtown'), (2, 'Mall');
INSERT INTO products (product_id, name, category) VALUES
    (1, 'Gadget', 'Electronics'),
    (2, 'Widget', 'Tools');

-- Sales on 2026-06-14 total 1500.0 (900.0 + 600.0); the 2026-06-13 row is excluded by date.
INSERT INTO sales (sale_id, product_id, branch_id, sale_date, qty, revenue) VALUES
    (1, 1, 1, '2026-06-14', 3, 900.0),
    (2, 2, 2, '2026-06-14', 4, 600.0),
    (3, 1, 1, '2026-06-13', 2, 500.0);

-- Widget (product 2) is out of stock at branch 1; Gadget is in stock.
INSERT INTO inventory (product_id, branch_id, on_hand) VALUES
    (1, 1, 10),
    (2, 1, 0);
