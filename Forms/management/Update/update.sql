-- Δημιουργία πίνακα users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    permissions INTEGER NOT NULL,
    creation_date_users TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα permissions
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Εισαγωγή βασικών δικαιωμάτων
INSERT INTO permissions (name)
SELECT 'admin' WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE name = 'admin');
INSERT INTO permissions (name)
SELECT 'user' WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE name = 'user');
INSERT INTO permissions (name)
SELECT 'viewer' WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE name = 'viewer');

-- Δημιουργία πίνακα user_permissions
CREATE TABLE IF NOT EXISTS user_permissions (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    permissions_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, permissions_id)
);

-- Δημιουργία πίνακα Brands (πρέπει να δημιουργηθεί ΠΡΙΝ τον πίνακα product)
CREATE TABLE IF NOT EXISTS Brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) UNIQUE,
    active BOOLEAN DEFAULT TRUE,
    creation_date_brand TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 
INSERT INTO Brands (brand_name,active)
VALUES ('',TRUE);


-- Δημιουργία πίνακα product
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    productcode VARCHAR(50) UNIQUE NOT NULL,
    pname VARCHAR(255),
    color VARCHAR(255),
    brand VARCHAR(255) NOT NULL,
    seasons VARCHAR(255) NOT NULL,
    size VARCHAR(50),
    material VARCHAR(255),
    description TEXT,
    buying_price DECIMAL(8,2) NOT NULL,
    sale_price INT NOT NULL,
    gross_profit DECIMAL(8,2) DEFAULT 0.00,
    price_per_unit DECIMAL(8,2),
    quantity INT NOT NULL CHECK (quantity >= 0.0),--CHECK (quantity >= 0.0)
    tax_percentage DECIMAL(8,2) CHECK (tax_percentage >= 0 AND tax_percentage <= 100),
    creation_date_product TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (brand) REFERENCES Brands(brand_name)
);

-- Δημιουργία πίνακα product_sale_item
CREATE TABLE IF NOT EXISTS product_sale_item (
    id SERIAL PRIMARY KEY,
    quantity_sold INT NOT NULL CHECK (quantity_sold > 0),
    price_per_unit DECIMAL(8,2) NOT NULL CHECK (price_per_unit >= 0),
    price DECIMAL(8,2) NOT NULL CHECK (price >= 0),
    tax_amount DECIMAL(8,2) NOT NULL CHECK (tax_amount >= 0),
    product_id INT NOT NULL,
    creation_date_product TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Δημιουργία πίνακα stock
CREATE TABLE IF NOT EXISTS stock (
    product_id INT NOT NULL PRIMARY KEY,
    in_stock DECIMAL(8,2) NOT NULL CHECK (in_stock >= 0),
    last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);