# LoanWise AI — Architecture

## Overview

LoanWise AI is a loan-management and financial-analysis application built around a layered architecture.

The application separates the user interface, business logic, financial calculations, database access, and persistence concerns.

## High-Level Architecture

```text
Streamlit UI
    │
    ▼
Services Layer
    │
    ├── Loan Service
    ├── Payment Service
    ├── Prepayment Service
    ├── Recommendation Service
    ├── Loan Analysis Service
    └── Loan Activity Service
    │
    ▼
Calculations Layer
    │
    ├── EMI
    ├── Amortization
    ├── Payment
    ├── Prepayment
    ├── Loan Analysis
    └── Recommendations
    │
    ▼
Repositories Layer
    │
    ├── Loan Repository
    ├── Payment Repository
    └── Related repositories
    │
    ▼
PostgreSQL Database
```

## Layer Responsibilities

### 1. Streamlit Application

`app/main.py` provides the interactive application interface.

Responsibilities include:

- displaying loan information
- accepting user input
- displaying analysis and recommendations
- recording payments and prepayments
- editing loan profiles
- archiving and closing loans
- exposing loan-management actions to the user

The UI delegates business operations to services instead of implementing database operations directly.

### 2. Services Layer

The service layer contains application-level business rules and validation.

Examples:

- `loan_service.py`
- `payment_service.py`
- `prepayment_service.py`
- `recommendation_service.py`
- `loan_analysis_service.py`
- `loan_activity_service.py`

Services validate input, retrieve required data, call calculations, and coordinate repository operations.

### 3. Calculations Layer

The calculations layer contains financial logic independently from the UI and database.

Examples include:

- EMI calculations
- amortization calculations
- payment calculations
- prepayment analysis
- remaining-loan analysis
- prepayment recommendations

Keeping calculations separate makes the financial logic easier to test and reuse.

### 4. Repositories Layer

Repositories are responsible for database access.

For example, the loan repository provides operations for:

- creating loans
- retrieving loans
- updating loan profiles
- updating balances
- archiving loans
- closing loans

Repositories use SQLAlchemy database connections and SQL statements.

### 5. Database

PostgreSQL stores the application's persistent data.

The loan-management system maintains loan profiles and associated financial activity such as EMI payments and prepayments.

## Request Flow

A typical operation follows this pattern:

```text
User Action
    ↓
Streamlit UI
    ↓
Service Validation
    ↓
Calculation / Business Logic
    ↓
Repository
    ↓
PostgreSQL
    ↓
Result
    ↓
Service
    ↓
Streamlit UI
```

This keeps database and business logic out of the presentation layer.

## Loan Lifecycle

Loans support several lifecycle states and actions.

```text
                ┌─────────────┐
                │    Active   │
                └──────┬──────┘
                       │
             ┌─────────┼──────────┐
             │         │          │
          Archive    Paid      Force Delete
             │         │          │
             ▼         ▼          ▼
        ┌──────────┐ ┌────────┐  Removed
        │ Archived │ │ Closed │
        └────┬─────┘ └────────┘
             │
          Unarchive
             │
             ▼
          Active
```

### Archive

Archiving removes a loan from normal active-loan workflows without permanently deleting its record.

### Unarchive

An archived loan can be restored to the active loan list through the application's loan-management interface.

### Close

A loan can be closed when its outstanding principal is zero.

### Force Delete

Force delete is the permanent removal operation. It is intended for removing an unwanted loan record and is distinct from archiving.

Because force deletion is destructive, it should be treated as an administrative/destructive action.

## Design Principles

### Separation of concerns

Each layer has a focused responsibility.

### Validation before persistence

User input is validated in services before database operations are performed.

### Reusable financial calculations

Financial formulas are kept independent from Streamlit and database code.

### Transactional database updates

Operations that create activity and update loan balances are handled together where required, helping maintain consistency.

### Testability

Business rules and calculations can be tested without relying on the Streamlit interface.

## Error Handling

The service layer raises `ValueError` for invalid application-level inputs and missing/invalid loan states.

The Streamlit layer catches these errors and presents user-readable messages.

## Testing

The project currently has a test suite covering the application's core functionality.

The finalized project checkpoint has passed:

```text
80 passed
```

Run the complete test suite with:

```powershell
pytest
```
