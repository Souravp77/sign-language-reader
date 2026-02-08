DROP DATABASE IF EXISTS expense_db;
CREATE DATABASE expense_db;
USE expense_db;

-- Table: users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(300) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: categories
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_name VARCHAR(50) NOT NULL,
    type ENUM('expense', 'income') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table: transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    type ENUM('expense', 'income') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

-- Table: budgets
CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount_limit DECIMAL(10,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

-- Insert default categories
INSERT INTO categories (category_name, type) VALUES
('Food & Dining', 'expense'),
('Transportation', 'expense'),
('Shopping', 'expense'),
('Entertainment', 'expense'),
('Bills & Utilities', 'expense'),
('Healthcare', 'expense'),
('Education', 'expense'),
('Rent/Mortgage', 'expense'),
('Travel', 'expense'),
('Gifts & Donations', 'expense'),
('Insurance', 'expense'),
('Other Expenses', 'expense'),
('Salary', 'income'),
('Freelance', 'income'),
('Business Income', 'income'),
('Investments', 'income'),
('Gifts Received', 'income'),
('Rental Income', 'income'),
('Refunds', 'income'),
('Other Income', 'income');