# LoanWise AI

LoanWise AI is a personal loan-management and financial-analysis application designed to help users manage multiple loans, track repayment activity, evaluate prepayments, and receive data-driven financial recommendations.

It combines a Streamlit interface, PostgreSQL persistence, a repository/service architecture, deterministic financial calculations, and an AI financial-advisor foundation.

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Application Workflow](#application-workflow)
- [Loan Management](#loan-management)
- [Payments and Prepayments](#payments-and-prepayments)
- [Financial Analysis](#financial-analysis)
- [Prepayment Recommendation](#prepayment-recommendation)
- [AI Financial Advisor](#ai-financial-advisor)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Database](#database)
- [Validation and Business Rules](#validation-and-business-rules)
- [Loan Lifecycle](#loan-lifecycle)
- [Testing](#testing)
- [Running the Project](#running-the-project)
- [Git Workflow](#git-workflow)
- [Design Principles](#design-principles)
- [Current Status](#current-status)
- [Future Scope](#future-scope)
- [Disclaimer](#disclaimer)

---

## Overview

LoanWise AI provides a structured view of a user's loans instead of treating each loan as only a monthly EMI.

The application maintains information including:

- Original principal
- Outstanding principal
- Interest rate
- Interest type
- EMI
- Original tenure
- Remaining tenure
- Loan start date
- EMI due day
- Processing charges
- Prepayment rules
- Prepayment charges
- Loan status
- EMI payment history
- Prepayment history

This information is used by the service and calculation layers to produce repayment insights and recommendations.

---

# Core Features

### Loan Management

- Register/add loans
- View user loans
- Edit loan profiles
- Archive loans
- Unarchive archived loans
- Close fully repaid loans
- Permanently force-delete loans
- Detect duplicate active loans

### Supported Loan Types

- Home
- Car
- Personal
- Education
- Business
- Other

### Supported Interest Types

- Fixed
- Floating

### Repayment

- Record EMI payments
- Track principal and interest components
- Track outstanding balance
- Mark late payments
- Track extra payments

### Prepayments

- Record prepayments
- Track principal before and after prepayment
- Estimate interest saved
- Estimate tenure reduction
- Maintain prepayment history

### Analysis

- Remaining-loan analysis
- Prepayment analysis
- Interest-saving calculations
- Tenure-reduction calculations
- Loan activity history
- Multi-loan prepayment recommendations

### AI

- AI financial-advisor foundation
- Structured financial context for future AI-assisted guidance

---

# Application Workflow

```text
User
  |
  v
Streamlit UI
  |
  v
Service Layer
  |
  +--------------------+
  |                    |
  v                    v
Calculation Layer   Repository Layer
  |                    |
  |                    v
  |                PostgreSQL
  |
  v
Financial Results
  |
  v
Streamlit UI
```

The UI is kept separate from the core financial logic so that calculations and business rules can be tested independently.

---

# Loan Management

## Registering a Loan

The main registration flow is:

```text
Enter loan details
       |
       v
Validate input
       |
       v
Check duplicate active loan
       |
       v
Create database record
       |
       v
Return created loan
```

The service entry point is:

```python
register_loan(...)
```

## Editing a Loan

Existing loan profile information can be edited through the application's **Edit Loan Profile** section.

The update operation supports fields such as:

- Loan name
- Loan type
- Lender
- Interest rate
- Interest type
- EMI
- Original tenure
- Loan start date
- EMI due day
- Processing charges
- Prepayment rules
- Prepayment charges

The service entry point is:

```python
update_loan_details(...)
```

Historical payment and prepayment records are not rewritten as part of a normal profile update.

## Duplicate Protection

Registration checks for a similar active loan using:

- User
- Loan name
- Lender
- Original principal
- Loan start date
- Active status

This helps prevent accidental duplicate active records.

---

# Payments and Prepayments

## EMI Payments

Payment records contain information such as:

- Payment date
- EMI amount
- Principal component
- Interest component
- Outstanding balance
- Late-payment flag
- Extra payment

The repository also supports a transactional operation that records a payment and updates the associated loan balance together.

## Prepayments

Prepayments are stored separately from regular EMI payments.

A prepayment can record:

- Payment date
- Amount
- Principal before
- Principal after
- Interest saved
- Tenure reduced
- Strategy

The loan's outstanding principal and remaining tenure are updated as part of the prepayment transaction.

## Combined Activity

LoanWise AI can combine EMI payments and prepayments into a single chronological activity history.

An activity can contain:

- Date
- Type
- Amount
- Principal paid
- Interest paid
- Extra payment
- Outstanding balance
- Interest saved
- Tenure reduced
- Late-payment status

The most recent activities are returned first.

---

# Financial Analysis

LoanWise AI has a dedicated calculation layer for remaining-loan analysis.

The analysis uses:

- Outstanding principal
- Annual interest rate
- Remaining tenure

The resulting analysis can provide:

- EMI
- Remaining interest
- Remaining repayment
- Remaining principal

The service entry point is:

```python
get_loan_analysis(loan_id)
```

The underlying calculation is separated into:

```python
analyze_remaining_loan(...)
```

This keeps financial calculations independent from Streamlit.

---

# Prepayment Recommendation

LoanWise AI can recommend which active loan should receive a proposed prepayment.

The workflow is:

```text
Proposed prepayment amount
            |
            v
Retrieve user's loans
            |
            v
Keep active loans
            |
            v
Ignore loans without outstanding principal
            |
            v
Analyze prepayment for each candidate
            |
            v
Compare interest savings
            |
            v
Rank candidates
            |
            v
Recommend highest-saving loan
```

The service function is:

```python
recommend_prepayment(
    user_id,
    prepayment_amount
)
```

The calculation layer uses:

```python
recommend_prepayment_target(...)
```

The current strategy is:

```text
maximum_interest_saving
```

The result contains:

- Recommended loan
- Candidate loans
- Interest rate
- Prepayment amount
- Estimated interest saved
- Estimated tenure reduction
- Strategy

---

# AI Financial Advisor

The project includes an AI financial-advisor foundation.

The AI layer is designed to work with structured information already maintained by LoanWise AI, including:

- Loan balances
- Interest rates
- EMIs
- Remaining tenure
- Payment activity
- Prepayments
- Interest-saving calculations
- Loan recommendations

The architecture keeps deterministic financial calculations separate from AI-generated explanations or guidance.

This allows financial numbers to remain reproducible while the AI layer can be used to explain results and assist with decision-making.

---

# Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Database | PostgreSQL |
| Database access | SQLAlchemy |
| Testing | pytest |
| Version control | Git / GitHub |
| AI | LLM / AI financial-advisor integration |

---

# Architecture

LoanWise AI follows a layered architecture:

```text
+----------------------+
|    Streamlit UI      |
|     app/main.py      |
+----------+-----------+
           |
           v
+----------------------+
|    Service Layer     |
|                      |
| loan_service         |
| payment_service      |
| prepayment_service   |
| recommendation...    |
| loan_analysis...     |
| loan_activity...     |
+-----+-----------+----+
      |           |
      v           v
+-----------+  +------------------+
|Calculation|  | Repository Layer |
|   Layer   |  |                  |
+-----------+  | Loan repository  |
               | Payment repo     |
               +--------+---------+
                        |
                        v
               +------------------+
               |   PostgreSQL DB   |
               +------------------+
```

## Layer Responsibilities

### UI Layer

Responsible for:

- User interaction
- Forms
- Dashboard presentation
- Displaying results
- Calling service functions

### Service Layer

Responsible for:

- Business rules
- Validation
- Orchestration
- Calling repositories and calculations

### Calculation Layer

Responsible for:

- EMI calculations
- Amortization
- Payment calculations
- Prepayment analysis
- Remaining-loan analysis
- Recommendations

### Repository Layer

Responsible for:

- Database queries
- Inserts
- Updates
- Retrieval
- Transactional persistence

---

# Project Structure

A simplified structure is:

```text
LoanWise AI/
│
├── app/
│   ├── main.py
│   └── main_backup.py
│
├── src/
│   ├── calculations/
│   │   ├── amortization.py
│   │   ├── emi.py
│   │   ├── loan_analysis.py
│   │   ├── payment.py
│   │   ├── prepayment.py
│   │   └── recommendations.py
│   │
│   ├── repositories/
│   │   ├── loan_repository.py
│   │   └── payment_repository.py
│   │
│   ├── services/
│   │   ├── loan_service.py
│   │   ├── loan_activity_service.py
│   │   ├── loan_analysis_service.py
│   │   ├── payment_service.py
│   │   ├── prepayment_service.py
│   │   └── recommendation_service.py
│   │
│   └── ...
│
├── tests/
│   ├── test_*.py
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Database

The primary loan records are stored in the `loans` table.

Important fields include:

```text
id
user_id
loan_name
loan_type
lender
original_principal
outstanding_principal
interest_rate
interest_type
emi
original_tenure_months
remaining_tenure_months
loan_start_date
emi_due_day
processing_charges
prepayment_rules
prepayment_charges
status
created_at
updated_at
```

Payment history is stored in:

```text
loan_payments
```

Prepayment history is stored in:

```text
prepayments
```

The repository layer handles database access, while the service layer applies business rules.

---

# Validation and Business Rules

Validation is performed before database operations.

## Identity

```text
user_id > 0
loan_id > 0
```

## Text Fields

```text
loan_name must not be empty
lender must not be empty
```

## Principal

```text
original_principal > 0
0 <= outstanding_principal <= original_principal
```

## Interest

```text
interest_rate >= 0
interest_type ∈ {fixed, floating}
```

## EMI

```text
emi > 0
```

## Tenure

```text
original_tenure_months > 0
0 <= remaining_tenure_months <= original_tenure_months
```

## EMI Due Day

When supplied:

```text
1 <= emi_due_day <= 31
```

## Charges

```text
processing_charges >= 0
prepayment_charges >= 0
```

## Loan Closing

A loan cannot be closed while:

```text
outstanding_principal > 0
```

An archived loan cannot be directly closed.

---

# Loan Lifecycle

Loan status is managed separately from the financial values.

```text
                 +----------+
                 |  Active  |
                 +----+-----+
                      |
             +--------+--------+
             |                 |
             v                 v
       +-----------+      +-----------+
       | Archived  |      |  Closed   |
       +-----+-----+      +-----------+
             |
             | Unarchive
             v
       +-----------+
       |  Active   |
       +-----------+
```

## Active

Normal loan-management and recommendation workflows operate on active loans.

## Archived

Archiving retains the loan record but removes it from normal active use.

An archived loan can later be unarchived through the application.

## Closed

A loan represents a closed/fully repaid state when its outstanding principal is zero.

## Force Delete

Force deletion is a permanent destructive operation.

It is separate from archiving and closing and is intended for situations where a loan record should actually be removed rather than retained.

---

# Testing

The project uses `pytest`.

The finalized development baseline currently passes:

```text
80 passed
```

The test suite covers areas including:

- Loan validation
- Loan registration
- Loan retrieval
- Loan updates
- Loan archiving
- Loan closing
- Payment behavior
- Prepayment behavior
- Loan activity
- Loan analysis
- Recommendation behavior
- Financial calculations

Run the full suite with:

```powershell
pytest
```

The expected baseline is all tests passing.

---

# Running the Project

## 1. Clone the repository

```powershell
git clone <repository-url>
cd "LoanWise AI"
```

Replace `<repository-url>` with the repository's actual GitHub URL.

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

## 3. Activate it

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

The terminal should show:

```text
(.venv)
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## 5. Configure PostgreSQL

LoanWise AI uses PostgreSQL.

Configure the database connection according to the project's database configuration/environment setup and ensure the required schema exists.

Do not commit database passwords or other secrets to Git.

## 6. Run tests

```powershell
pytest
```

## 7. Start Streamlit

From the project root:

```powershell
streamlit run app/main.py
```

Streamlit will display the local application address in the terminal.

---

# Git Workflow

Recommended development workflow:

```text
Make change
    |
    v
Run pytest
    |
    v
Check git diff
    |
    v
Run/verify application
    |
    v
git add .
    |
    v
git commit
    |
    v
git push
```

Useful commands:

```powershell
git status
git diff
git add .
git commit -m "description of change"
git push
```

Before a release/checkpoint:

```powershell
pytest
git status
git log --oneline -5
```

---

# Design Principles

## Separation of concerns

UI, services, repositories, and calculations are kept in separate layers.

## Deterministic financial logic

Financial calculations live outside the Streamlit UI and can therefore be tested independently.

## Service-level validation

Business rules are checked before database operations.

## Transactional updates

Related financial database operations are performed transactionally where appropriate.

For example, recording a payment can insert the payment and update the loan balance in the same database transaction.

## Historical records

Payments and prepayments are retained as historical activities rather than relying only on the current loan balance.

## Safe lifecycle management

Archiving, closing, and deleting have different meanings:

- **Archive:** retain the record but remove it from normal active use.
- **Close:** represent a fully repaid loan.
- **Force delete:** permanently remove the record.

---

# Current Status

LoanWise AI has reached a stable feature-complete baseline for its current scope.

Implemented functionality includes:

- Loan registration
- Comprehensive loan validation
- Duplicate active-loan detection
- Loan editing
- Loan dashboard
- Loan archiving
- Loan unarchiving
- Loan closing
- Force deletion
- EMI payment recording
- Prepayment recording
- Combined loan activity
- Remaining-loan analysis
- Prepayment analysis
- Interest-saving calculations
- Tenure-reduction calculations
- Prepayment recommendations
- PostgreSQL persistence
- AI financial-advisor foundation
- Automated tests

Current test baseline:

```text
80 passed
```

The project is now positioned as a stable baseline for documentation, demonstration, and future feature development.

---

# Future Scope

Potential future improvements include:

- More advanced AI financial planning
- Cash-flow-aware repayment recommendations
- Goal-based debt reduction
- Loan comparison
- Amortization visualizations
- Financial reports and exports
- Automated financial summaries
- Authentication and stronger multi-user support
- More comprehensive audit/history controls
- Database migration management
- Production deployment
- Additional financial products and planning tools

These are future possibilities and are not required for the current stable baseline.

---

# Disclaimer

LoanWise AI is a financial-management and decision-support application.

Results depend on the accuracy of the loan information entered into the application. Calculations and recommendations should not be treated as a replacement for official lender statements, loan agreements, or professional financial advice.

For important decisions involving repayment, foreclosure, prepayment charges, interest rates, or loan restructuring, verify the applicable terms with the relevant lender.

---

# Project Summary

LoanWise AI brings loan management, repayment tracking, financial calculations, prepayment analysis, and AI-assisted financial guidance into one application.

The core architecture is:

```text
Streamlit
    ↓
Services
    ↓
Calculations + Repositories
    ↓
PostgreSQL
```

The architecture is intentionally modular so the UI, business logic, financial calculations, database layer, and AI capabilities can evolve independently.
