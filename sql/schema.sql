-- ============================================================
-- LoanWise AI - Initial Database Schema
-- ============================================================


-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- LOANS
-- ============================================================

CREATE TABLE loans (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    loan_name VARCHAR(150) NOT NULL,
    loan_type VARCHAR(30) NOT NULL,
    lender VARCHAR(150) NOT NULL,

    original_principal NUMERIC(15, 2) NOT NULL
        CHECK (original_principal > 0),

    outstanding_principal NUMERIC(15, 2) NOT NULL
        CHECK (outstanding_principal >= 0),

    interest_rate NUMERIC(6, 3) NOT NULL
        CHECK (interest_rate >= 0),

    interest_type VARCHAR(20) NOT NULL,

    emi NUMERIC(15, 2) NOT NULL
        CHECK (emi > 0),

    original_tenure_months INTEGER NOT NULL
        CHECK (original_tenure_months > 0),

    remaining_tenure_months INTEGER NOT NULL
        CHECK (remaining_tenure_months >= 0),

    loan_start_date DATE NOT NULL,

    emi_due_day INTEGER
        CHECK (emi_due_day BETWEEN 1 AND 31),

    processing_charges NUMERIC(15, 2) NOT NULL DEFAULT 0
        CHECK (processing_charges >= 0),

    prepayment_rules TEXT,

    prepayment_charges NUMERIC(15, 2) NOT NULL DEFAULT 0
        CHECK (prepayment_charges >= 0),

    status VARCHAR(20) NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT loans_loan_type_check
        CHECK (
            loan_type IN (
                'home',
                'car',
                'personal',
                'education',
                'business',
                'other'
            )
        ),

    CONSTRAINT loans_interest_type_check
        CHECK (
            interest_type IN (
                'fixed',
                'floating'
            )
        ),

    CONSTRAINT loans_status_check
        CHECK (
            status IN (
                'active',
                'closed',
                'archived'
            )
        ),

    CONSTRAINT loans_outstanding_not_above_original
        CHECK (
            outstanding_principal <= original_principal
        )
);


-- ============================================================
-- LOAN PAYMENTS
-- ============================================================

CREATE TABLE loan_payments (
    id BIGSERIAL PRIMARY KEY,
    loan_id BIGINT NOT NULL REFERENCES loans(id) ON DELETE CASCADE,

    payment_date DATE NOT NULL,

    emi_amount NUMERIC(15, 2) NOT NULL
        CHECK (emi_amount > 0),

    principal_component NUMERIC(15, 2) NOT NULL
        CHECK (principal_component >= 0),

    interest_component NUMERIC(15, 2) NOT NULL
        CHECK (interest_component >= 0),

    outstanding_balance NUMERIC(15, 2) NOT NULL
        CHECK (outstanding_balance >= 0),

    late_payment BOOLEAN NOT NULL DEFAULT FALSE,

    extra_payment NUMERIC(15, 2) NOT NULL DEFAULT 0
        CHECK (extra_payment >= 0),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- PREPAYMENTS
-- ============================================================

CREATE TABLE prepayments (
    id BIGSERIAL PRIMARY KEY,
    loan_id BIGINT NOT NULL REFERENCES loans(id) ON DELETE CASCADE,

    payment_date DATE NOT NULL,

    amount NUMERIC(15, 2) NOT NULL
        CHECK (amount > 0),

    principal_before NUMERIC(15, 2) NOT NULL
        CHECK (principal_before >= 0),

    principal_after NUMERIC(15, 2) NOT NULL
        CHECK (principal_after >= 0),

    interest_saved NUMERIC(15, 2)
        CHECK (interest_saved >= 0),

    tenure_reduced_months INTEGER
        CHECK (tenure_reduced_months >= 0),

    strategy VARCHAR(30),

    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT prepayments_principal_reduction_check
        CHECK (
            principal_after <= principal_before
        )
);


-- ============================================================
-- INTEREST RATE HISTORY
-- ============================================================

CREATE TABLE interest_rate_history (
    id BIGSERIAL PRIMARY KEY,
    loan_id BIGINT NOT NULL REFERENCES loans(id) ON DELETE CASCADE,

    interest_rate NUMERIC(6, 3) NOT NULL
        CHECK (interest_rate >= 0),

    effective_from DATE NOT NULL,
    effective_to DATE,

    reason VARCHAR(255),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT interest_rate_dates_check
        CHECK (
            effective_to IS NULL
            OR effective_to >= effective_from
        )
);


-- ============================================================
-- CREDIT SCORE HISTORY
-- ============================================================

CREATE TABLE credit_score_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    score INTEGER NOT NULL
        CHECK (score BETWEEN 1 AND 900),

    recorded_date DATE NOT NULL,

    credit_utilization NUMERIC(5, 2)
        CHECK (
            credit_utilization >= 0
            AND credit_utilization <= 100
        ),

    active_loans INTEGER
        CHECK (active_loans >= 0),

    credit_cards INTEGER
        CHECK (credit_cards >= 0),

    recent_enquiries INTEGER
        CHECK (recent_enquiries >= 0),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- SCENARIOS
-- ============================================================

CREATE TABLE scenarios (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    scenario_name VARCHAR(150) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL,

    input_data JSONB NOT NULL,
    result_data JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_loans_user_id
    ON loans(user_id);

CREATE INDEX idx_loans_status
    ON loans(status);

CREATE INDEX idx_loan_payments_loan_id
    ON loan_payments(loan_id);

CREATE INDEX idx_loan_payments_payment_date
    ON loan_payments(payment_date);

CREATE INDEX idx_prepayments_loan_id
    ON prepayments(loan_id);

CREATE INDEX idx_prepayments_payment_date
    ON prepayments(payment_date);

CREATE INDEX idx_interest_rate_history_loan_id
    ON interest_rate_history(loan_id);

CREATE INDEX idx_credit_score_history_user_id
    ON credit_score_history(user_id);

CREATE INDEX idx_credit_score_history_recorded_date
    ON credit_score_history(recorded_date);

CREATE INDEX idx_scenarios_user_id
    ON scenarios(user_id);