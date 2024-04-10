-- Create Departments Table
CREATE TABLE IF NOT EXISTS departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL
);

-- Create Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE SET NULL
);

-- Create Projects Table
CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE CASCADE
);

-- Insert sample data into Departments
INSERT INTO departments (department_name) VALUES ('Human Resources'), ('Engineering'), ('Marketing');

-- Insert sample data into Employees
INSERT INTO employees (first_name, last_name, department_id) VALUES
('John', 'Doe', 1),
('Jane', 'Doe', 2),
('Jim', 'Beam', 3);

-- Insert sample data into Projects
INSERT INTO projects (project_name, start_date, end_date, department_id) VALUES
('Hiring Plan 2024', '2023-07-01', '2024-06-30', 1),
('New Product Development', '2023-09-01', '2024-08-31', 2),
('Social Media Campaign', '2023-10-15', '2024-01-15', 3);
