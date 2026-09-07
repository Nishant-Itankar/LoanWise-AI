# LoanWise AI — Technical Architecture

## 1. Purpose

This document describes the technical architecture of **LoanWise AI**, including its application layers, data flow, loan lifecycle, financial calculation modules, database interaction, validation, and testing structure.

The architecture is based on the finalized project implementation.

---

## 2. High-Level Architecture

LoanWise AI follows a layered Python application architecture:

```text
┌───────────────────────────────┐
│        Streamlit UI           │
│          app/main.py          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Service Layer          │
│   src/services/*.py            │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐  ┌────────────────┐
│ Repository    │  │ Calculation    │
│ Layer         │  │ Layer          │
│ repositories/ │  │ calculations/  │
└───────┬───────┘  └────────────────┘
        │
        ▼
┌───────────────────────────────┐
│          Database             │
│          PostgreSQL           │
└───────────────────────────────┘
```

The main architectural separation is:

- **UI** handles interaction and presentation.
- **Services** handle application/business workflows and validation.
- **Repositories** handle database access.
- **Calculations** handle financial mathematics independently from the UI/database.
- **Database** persists loan, payment, and prepayment data.

---

## 3. Project Structure

The important project areas are organized approximately as follows:

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
│   │   ├── recommendation_service.py
│   │   ├── payment_service.py
│   │   ├── prepayment_service.py
│   │   ├── dashboard_service.py
│   │   └── user_service.py
│   │
│   └── utils/
│
├── tests/
│
├── README.md
└── docs/
    └── ARCHITECTURE.md
```

The exact contents may grow as additional features are added, but the architectural responsibility of each layer remains the same.

---

# 4. Application Layer

## 4.1 Streamlit Application

The primary user interface is implemented in:

```text
app/main.py
```

The Streamlit application provides access to:

- User selection
- Loan registration
- Loan overview
- Loan analysis
- Loan activity
- EMI payment recording
- Prepayment recording
- Prepayment recommendations
- Loan profile editing
- Loan archiving
- Loan closing
- Loan unarchiving
- Force deletion

The UI calls service functions instead of directly implementing database queries.

For example:

```text
Streamlit UI
     ↓
register_loan()
     ↓
loan_service.py
     ↓
loan_repository.py
     ↓
PostgreSQL
```

This keeps database implementation details outside the UI.

---

# 5. Service Layer

The service layer contains application-level business logic.

## 5.1 Loan Service

```text
src/services/loan_service.py
```

The loan service handles:

- Loan registration
- Loan validation
- Duplicate-loan detection
- Loan retrieval
- Loan summaries
- Loan profile updates
- Loan archiving
- Loan closing
- Loan lifecycle rules

Important validation includes:

- User ID must be positive.
- Loan name cannot be empty.
- Lender cannot be empty.
- Loan type must be supported.
- Interest type must be supported.
- Principal values must be valid.
- Outstanding principal cannot exceed original principal.
- EMI must be greater than zero.
- Tenure values must be valid.
- Remaining tenure cannot exceed original tenure.
- EMI due day must be between 1 and 31 when supplied.
- Processing/prepayment charges cannot be negative.

Supported loan types are:

```text
home
car
personal
education
business
other
```

Supported interest types are:

```text
fixed
floating
```

---

## 5.2 Loan Activity Service

```text
src/services/loan_activity_service.py
```

This service provides a unified view of loan activity.

It combines:

- EMI payments
- Prepayments

into a common activity representation.

Activities are sorted by date and ID in descending order so that the latest activity appears first.

The activity representation includes fields such as:

```text
date
type
amount
principal_paid
interest_paid
extra_payment
outstanding_balance
interest_saved
tenure_reduced_months
late_payment
```

This allows the UI to present EMI and prepayment history together.

---

## 5.3 Loan Analysis Service

```text
src/services/loan_analysis_service.py
```

This service retrieves a loan and passes its current financial state to the remaining-loan calculation engine.

The returned analysis includes:

- EMI used for analysis
- Remaining interest
- Remaining repayment
- Remaining principal

The service is intentionally separate from the calculation module.

---

## 5.4 Recommendation Service

```text
src/services/recommendation_service.py
```

The recommendation service:

1. Retrieves loans for a user.
2. Filters to active loans.
3. Validates the requested prepayment amount.
4. Sends eligible loans to the recommendation calculation.
5. Returns the recommended target and candidate comparison.

The current strategy is:

```text
maximum_interest_saving
```

The recommendation engine evaluates the eligible loans and ranks candidates according to estimated interest savings.

---

# 6. Repository Layer

Repositories isolate database operations from business logic.

## 6.1 Loan Repository

```text
src/repositories/loan_repository.py
```

The loan repository provides operations including:

- Create loan
- Get loan by ID
- Get loans by user
- Find active duplicate loan
- Archive loan
- Close loan
- Update loan
- Update loan balance

SQL operations are executed through SQLAlchemy's engine and `text()` queries.

Database mutations use:

```python
with engine.begin() as connection:
```

This provides transaction handling for write operations.

---

## 6.2 Payment Repository

```text
src/repositories/payment_repository.py
```

The payment repository handles:

- EMI payment creation
- EMI payment retrieval
- EMI payment + loan balance update
- Prepayment creation + loan balance update
- Prepayment retrieval

The combined payment/update operations are executed inside a database transaction.

This is important because the payment record and the corresponding loan state should be updated together.

---

# 7. Database Interaction

The application uses PostgreSQL as its persistent database.

The principal loan record contains information such as:

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

Payment records maintain the historical payment information, including:

```text
loan_id
payment_date
emi_amount
principal_component
interest_component
outstanding_balance
late_payment
extra_payment
```

Prepayment records maintain:

```text
loan_id
payment_date
amount
principal_before
principal_after
interest_saved
tenure_reduced_months
strategy
```

---

# 8. Loan Lifecycle

A loan has a status representing its lifecycle.

The principal lifecycle is:

```text
                 ┌─────────────┐
                 │   Active    │
                 └──────┬──────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌─────────────┐     ┌─────────────┐
       │  Archived   │     │   Closed    │
       └──────┬──────┘     └─────────────┘
              │
              │ Unarchive
              ▼
       ┌─────────────┐
       │   Active    │
       └─────────────┘
```

## Active

An active loan is part of the normal loan-management workflow and can participate in calculations such as prepayment recommendations.

## Archived

Archiving removes the loan from normal active usage without permanently deleting its record.

Archived loans can later be restored through the unarchive workflow.

## Closed

A loan can be closed when its outstanding principal has reached zero.

The close operation sets:

```text
status = closed
outstanding_principal = 0
remaining_tenure_months = 0
```

A loan with outstanding principal cannot be closed through the normal close workflow.

---

# 9. Archive and Unarchive

Archiving is intentionally different from deletion.

```text
Active
  │
  └── Archive
        ↓
     Archived
        │
        └── Unarchive
              ↓
           Active
```

The purpose is to allow users to temporarily remove a loan from normal usage while preserving its historical data.

This is particularly useful when a loan is no longer being actively tracked but may need to be restored later.

---

# 10. Force Delete

Force deletion is a destructive loan-management operation.

It is intentionally different from:

- Archive
- Close

The conceptual distinction is:

```text
Archive → hide/preserve
Close   → completed loan
Delete  → permanently remove
```

Force deletion is intended for situations where the user explicitly wants to remove a loan record rather than preserve it.

Because deletion is destructive, it should be exposed as an explicit action in the application rather than being part of normal loan lifecycle operations.

The finalized application supports force deletion for loan management, including loans with outstanding principal.

---

# 11. Duplicate Loan Protection

Loan registration checks for an active duplicate before creating a new record.

The duplicate check compares:

- User
- Loan name
- Lender
- Original principal
- Loan start date
- Active status

The repository performs the database lookup while the service layer decides whether registration should proceed.

This prevents accidental duplicate active loans while still allowing historical/archived records to exist.

---

# 12. Financial Calculation Layer

Financial mathematics is kept separate from Streamlit and database code.

The main calculation modules include:

```text
src/calculations/
```

### EMI

```text
emi.py
```

Handles EMI-related financial calculations.

### Amortization

```text
amortization.py
```

Handles repayment schedules and principal/interest allocation.

### Loan Analysis

```text
loan_analysis.py
```

Analyzes the remaining loan based on:

- Outstanding principal
- Interest rate
- Remaining tenure

### Payment Calculation

```text
payment.py
```

Supports payment-related financial calculations.

### Prepayment Analysis

```text
prepayment.py
```

Evaluates the financial effect of making a prepayment, including estimated:

- Interest savings
- Tenure reduction

### Recommendation Calculation

```text
recommendations.py
```

Compares eligible loans and selects the prepayment target using the maximum-interest-saving strategy.

---

# 13. Payment Flow

An EMI payment follows this general flow:

```text
User enters payment
        ↓
Streamlit
        ↓
Payment Service
        ↓
Payment Calculation
        ↓
Payment Repository
        ↓
┌─────────────────────────────┐
│ Insert payment record       │
│ Update loan balance         │
│ Update remaining tenure     │
└─────────────────────────────┘
        ↓
     Database
```

The payment and loan update are performed within the same database transaction.

---

# 14. Prepayment Flow

A prepayment follows:

```text
User enters prepayment
        ↓
Streamlit
        ↓
Prepayment Service
        ↓
Prepayment Calculation
        ↓
┌──────────────────────────────┐
│ Calculate new loan state     │
│ Calculate interest savings   │
│ Calculate tenure reduction   │
└──────────────────────────────┘
        ↓
Prepayment Repository
        ↓
┌──────────────────────────────┐
│ Insert prepayment record     │
│ Update loan balance          │
│ Update remaining tenure      │
└──────────────────────────────┘
        ↓
     Database
```

---

# 15. Recommendation Flow

The prepayment recommendation workflow is:

```text
User
 │
 │ prepayment amount
 ▼
Recommendation Service
 │
 │ retrieve user loans
 ▼
Filter active loans
 │
 ▼
Recommendation Calculation
 │
 ├── evaluate Loan A
 ├── evaluate Loan B
 ├── evaluate Loan C
 └── ...
 │
 ▼
Rank by interest saved
 │
 ▼
Recommended Loan
```

The calculation skips loans whose outstanding principal is not positive.

The returned result contains:

```text
recommended_loan
candidates
strategy
```

---

# 16. Error Handling

The service layer uses explicit `ValueError` exceptions for invalid application inputs.

Examples include:

```text
Loan ID must be positive.
Loan not found.
Loan name cannot be empty.
Lender cannot be empty.
Invalid loan type.
Invalid interest type.
Interest rate cannot be negative.
EMI must be greater than zero.
Original tenure must be greater than zero.
Remaining tenure cannot exceed original tenure.
Outstanding principal cannot exceed original principal.
Loan cannot be closed while outstanding principal exists.
```

The Streamlit application catches these errors and displays user-facing error messages.

Unexpected exceptions are separately caught by the UI where appropriate so that database/application errors do not crash the entire interface.

---

# 17. Separation of Responsibilities

The project intentionally avoids putting all logic inside `app/main.py`.

### UI Layer

Responsible for:

- Input controls
- Forms
- Buttons
- Display
- User-facing errors
- Calling services

### Service Layer

Responsible for:

- Validation
- Workflow orchestration
- Business rules
- Selecting which repository/calculation operation to call

### Repository Layer

Responsible for:

- SQL
- Database reads
- Database writes
- Transactions

### Calculation Layer

Responsible for:

- Financial mathematics
- Loan analysis
- Prepayment analysis
- Recommendations

This separation makes the project easier to test and maintain.

---

# 18. Testing Architecture

The project includes automated tests under:

```text
tests/
```

The finalized project currently has:

```text
80 passed
```

The test suite covers service, calculation, repository-related behavior, validation, loan activity, analysis, recommendation behavior, and other application functionality implemented in the project.

A successful test run should report:

```text
80 passed
```

Tests should be run before major commits and after changes to core loan-management or calculation logic.

---

# 19. Database Safety and Transactions

Operations that modify multiple related records use a transaction.

For example, recording an EMI payment involves:

```text
INSERT loan_payments
        +
UPDATE loans
```

Both operations occur within one transaction.

Likewise, a prepayment involves:

```text
INSERT prepayments
        +
UPDATE loans
```

If the transaction fails, the database can roll back the operation instead of leaving the payment history and loan balance inconsistent.

---

# 20. Data Consistency Rules

Important consistency rules enforced by the application include:

### Principal

```text
original_principal > 0
0 <= outstanding_principal <= original_principal
```

### Tenure

```text
original_tenure_months > 0
0 <= remaining_tenure_months <= original_tenure_months
```

### EMI

```text
emi > 0
```

### Interest rate

```text
interest_rate >= 0
```

### EMI due day

```text
1 <= emi_due_day <= 31
```

when a due day is provided.

### Charges

```text
processing_charges >= 0
prepayment_charges >= 0
```

---

# 21. Current Architectural State

The finalized application contains the core building blocks required for a functional loan-management system:

- Loan registration
- Loan validation
- Loan editing
- Duplicate detection
- Loan analysis
- EMI payment recording
- Prepayment recording
- Combined activity history
- Interest-saving analysis
- Prepayment recommendations
- Loan archiving
- Loan unarchiving
- Loan closing
- Force deletion
- PostgreSQL persistence
- Automated testing
- AI financial-advisor foundation

The project currently represents a layered financial application rather than a single-file Streamlit prototype.

---

# 22. Future Extension Points

The existing separation makes future additions possible without redesigning the entire application.

Potential extension areas include:

- More advanced recommendation strategies
- Multiple prepayment strategies
- Detailed amortization visualization
- Financial dashboards
- Export/report generation
- More comprehensive audit history
- Authentication and authorization
- Additional AI advisor capabilities
- Automated financial summaries
- Additional loan and repayment scenarios

These are extension points rather than claims about functionality currently implemented.

---

# 23. Development Principle

The central architectural principle of LoanWise AI is:

```text
Keep presentation,
business logic,
database access,
and financial calculations
separate.
```

This allows the financial calculation engine to be tested independently, database operations to be changed without rewriting the UI, and the Streamlit application to remain focused on user interaction.

---

## 24. Documentation Relationship

The project documentation is intentionally divided into separate levels:

```text
README.md
    ↓
Project overview
Features
Setup
Usage
Testing
Project status

docs/ARCHITECTURE.md
    ↓
Technical architecture
Layers
Data flow
Database interaction
Lifecycle
Calculations
Design decisions
```

`README.md` is the entry point for users and reviewers.

`ARCHITECTURE.md` is the technical reference for understanding how the application is implemented.
