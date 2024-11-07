-- SCHEMA: fintech
CREATE SCHEMA IF NOT EXISTS fintech;

-- Table: fintech.employer
CREATE TABLE fintech.employer (
    id uuid PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    contact_email VARCHAR(254),
    contact_phone VARCHAR(15)
);

-- Table: fintech.employee
CREATE TABLE fintech.employee (
    id uuid PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    employer_id UUID NOT NULL REFERENCES fintech.employer(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    phone VARCHAR(15),
    salary DECIMAL(10, 2) CHECK (salary >= 0)
);

-- Table: fintech.salary_advance_request
CREATE TABLE fintech.salary_advance_request (
    id uuid PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    employee_id UUID NOT NULL REFERENCES fintech.employee(id) ON DELETE CASCADE,
    amount_requested DECIMAL(10, 2) CHECK (amount_requested >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'approved', 'rejected')),
    request_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    review_date TIMESTAMPTZ
);

-- Table: fintech.transaction
CREATE TABLE fintech.transaction (
    id uuid PRIMARY KEY,
    request_id UUID NOT NULL REFERENCES fintech.salary_advance_request(id) ON DELETE CASCADE,
    transaction_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    amount DECIMAL(10, 2) CHECK (amount >= 0)
);

-- Indexes and constraints
CREATE INDEX idx_employee_employer ON fintech.employee (employer_id);
CREATE INDEX idx_request_employee ON fintech.salary_advance_request (employee_id);
CREATE INDEX idx_transaction_request ON fintech.transaction (request_id);
