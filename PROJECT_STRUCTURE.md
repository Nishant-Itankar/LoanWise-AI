# LoanWise AI — Project Structure

## Overview

LoanWise AI is organized into application, service, calculation, repository, utility, and test layers.

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
│   │   ├── payment_repository.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── loan_service.py
│   │   ├── payment_service.py
│   │   ├── prepayment_service.py
│   │   ├── recommendation_service.py
│   │   ├── loan_analysis_service.py
│   │   ├── loan_activity_service.py
│   │   └── ...
│   │
│   ├── utils/
│   │   └── ...
│   │
│   └── database.py
│
├── tests/
│   ├── test_loan_activity_service.py
│   ├── test_loan_analysis_service.py
│   ├── test_recommendation_service.py
│   └── ...
│
├── README.md
├── API_REFERENCE.md
├── ARCHITECTURE.md
├── DATABASE.md
├── DEVELOPMENT.md
├── PROJECT_STRUCTURE.md
└── CHANGELOG.md
```

## `app/`

Contains the Streamlit presentation layer.

### `main.py`

The primary application entry point.

It handles:

- application pages/UI
- loan selection
- loan registration
- loan editing
- payment/prepayment workflows
- analysis display
- recommendations
- archive/close/delete-related UI actions

The UI delegates core operations to service functions.

## `src/calculations/`

Contains financial calculations.

### `emi.py`

EMI-related calculations.

### `amortization.py`

Amortization schedule calculations.

### `payment.py`

Payment-related calculations.

### `prepayment.py`

Prepayment impact calculations, including interest savings and tenure reduction.

### `loan_analysis.py`

Remaining-loan analysis.

### `recommendations.py`

Prepayment-target recommendation logic.

## `src/services/`

Contains application business logic.

Services validate inputs and coordinate calculations and repositories.

Important services include:

- Loan Service
- Payment Service
- Prepayment Service
- Recommendation Service
- Loan Analysis Service
- Loan Activity Service

## `src/repositories/`

Contains database access.

Repositories isolate SQL/database operations from the rest of the application.

## `src/database.py`

Provides database connectivity/configuration used by repositories.

## `src/utils/`

Contains reusable utility functionality that does not belong to the core calculation or service layers.

## `tests/`

Contains automated tests for application behavior.

The finalized project checkpoint has passed:

```text
80 passed
```

## Architectural Boundary

The intended dependency direction is:

```text
app
 ↓
services
 ↓
calculations / repositories
 ↓
database
```

The UI should not bypass services to perform business operations directly.

## Adding New Functionality

For a new feature, prefer:

```text
UI
 ↓
Service
 ↓
Calculation (if financial logic is needed)
 ↓
Repository
 ↓
Database
```

Then add tests for validation, business logic, and integration behavior as appropriate.
