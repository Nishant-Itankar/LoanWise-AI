# LoanWise AI — API & Service Reference

## 1. Purpose

This document is the developer reference for the application-level services and core calculation interfaces in LoanWise AI.

The project uses a layered design:

```text
Streamlit UI
     ↓
Service Layer
     ↓
Repository / Calculation Layer
     ↓
PostgreSQL / Financial Calculations
```

The service layer is the preferred application interface for the Streamlit UI.

---

# 2. Loan Service

File:

```text
src/services/loan_service.py
```

## `register_loan(...)`

Registers a new loan after validating the supplied loan information and checking for an active duplicate.

### Parameters

```text
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
```

### Validation

The service validates:

- Positive user ID
- Non-empty loan name
- Non-empty lender
- Valid loan type
- Valid interest type
- Positive original principal
- Non-negative outstanding principal
- Outstanding principal not greater than original principal
- Non-negative interest rate
- Positive EMI
- Positive original tenure
- Non-negative remaining tenure
- Remaining tenure not greater than original tenure
- EMI due day between 1 and 31 when supplied
- Non-negative processing charges
- Non-negative prepayment charges

It also checks for an active duplicate loan using:

```text
user_id
loan_name
lender
original_principal
loan_start_date
```

### Returns

The created loan record returned by the repository.

### Errors

Raises `ValueError` for invalid input or an active duplicate loan.

---

## `validate_loan(...)`

Validates core loan financial fields.

### Parameters

```text
loan_type
interest_type
original_principal
outstanding_principal
interest_rate
emi
original_tenure_months
remaining_tenure_months
```

### Returns

No explicit value on success.

### Errors

Raises `ValueError` when a validation rule fails.

---

## `get_loan(loan_id)`

Retrieves a loan by ID.

### Validation

```text
loan_id > 0
```

### Returns

The loan record, or the repository result when no record is found.

---

## `get_user_loans(user_id)`

Retrieves loans belonging to a user.

### Validation

```text
user_id > 0
```

### Returns

The user's loan records.

---

## `get_user_loan_summary(user_id)`

Returns a simplified representation of the user's loans.

### Returned fields

```text
id
loan_name
loan_type
lender
outstanding_principal
interest_rate
emi
remaining_tenure_months
status
```

Numeric database values are converted to Python numeric values where required.

---

## `update_loan_details(...)`

Updates the editable profile information of an existing loan.

### Parameters

```text
loan_id
loan_name
loan_type
lender
interest_rate
interest_type
emi
original_tenure_months
loan_start_date
emi_due_day
processing_charges
prepayment_rules
prepayment_charges
```

### Validation

Validates:

- Loan ID
- Loan name
- Lender
- Loan type
- Interest type
- Interest rate
- EMI
- Original tenure
- EMI due day
- Processing charges
- Prepayment charges

### Returns

The updated loan record from the repository.

---

## `archive_user_loan(loan_id)`

Archives an existing loan.

### Behavior

- Rejects invalid loan IDs.
- Rejects missing loans.
- Rejects loans already archived.
- Calls the repository archive operation.

### Returns

The updated loan record.

---

## `close_user_loan(loan_id)`

Closes a loan.

### Preconditions

The loan must:

- Exist
- Not already be closed
- Not be archived
- Have zero outstanding principal

### Important rule

A loan with outstanding principal cannot be closed through this operation.

### Returns

The updated closed loan record.

---

# 3. Loan Activity Service

File:

```text
src/services/loan_activity_service.py
```

## `get_loan_activity(loan_id)`

Retrieves EMI payment activity for a loan.

### Returned fields

```text
id
loan_id
payment_date
emi_amount
principal_component
interest_component
outstanding_balance
late_payment
extra_payment
```

Numeric monetary values are returned as Python floats.

---

## `get_loan_activity_summary(loan_id)`

Creates an aggregate summary of EMI payment activity.

### Returned fields

```text
loan_id
payment_count
total_emi_paid
total_principal_paid
total_interest_paid
total_extra_payments
latest_outstanding_balance
```

When no payment exists, the current loan outstanding principal is used as the latest outstanding balance.

---

## `get_combined_loan_activity(loan_id)`

Combines EMI payments and prepayments into one activity list.

### Activity types

```text
EMI Payment
Prepayment
```

### Common activity fields

```text
id
loan_id
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

Activities are sorted by date and ID in descending order.

This allows the UI to display repayment history as a single chronological activity stream.

---

# 4. Loan Analysis Service

File:

```text
src/services/loan_analysis_service.py
```

## `get_loan_analysis(loan_id)`

Retrieves a loan and analyzes its remaining repayment position.

### Inputs

```text
loan_id
```

### Validation

```text
loan_id > 0
loan must exist
```

### Analysis inputs

The service passes these loan values to the calculation engine:

```text
outstanding_principal
interest_rate
remaining_tenure_months
```

### Returned structure

```text
loan_id
loan_name
interest_rate
interest_type
emi
remaining_tenure_months
outstanding_principal
analysis
```

The `analysis` object contains the calculation result supplied by the remaining-loan analysis engine.

---

# 5. Recommendation Service

File:

```text
src/services/recommendation_service.py
```

## `recommend_prepayment(user_id, prepayment_amount)`

Recommends a loan on which a user should make a prepayment.

### Validation

```text
user_id > 0
prepayment_amount > 0
```

### Workflow

```text
Get user's loans
       ↓
Filter active loans
       ↓
Recommendation calculation
       ↓
Rank candidates
       ↓
Return recommendation
```

Only active loans are passed to the recommendation calculation.

### Returns

A recommendation result containing:

```text
recommended_loan
candidates
strategy
```

The current strategy is:

```text
maximum_interest_saving
```

---

# 6. Payment Service

File:

```text
src/services/payment_service.py
```

The payment service is responsible for the application workflow around recording and retrieving loan payments.

Its responsibilities include:

- Accepting payment information from the application.
- Applying payment calculations.
- Recording payment information.
- Updating the corresponding loan balance.
- Providing payment history.

Payment persistence and loan-balance updates are handled through repository operations designed to execute as a transaction.

---

# 7. Prepayment Service

File:

```text
src/services/prepayment_service.py
```

The prepayment service manages the workflow for recording loan prepayments.

Its responsibilities include:

- Accepting prepayment information.
- Calculating the financial effect of the prepayment.
- Recording the prepayment.
- Updating outstanding principal.
- Updating remaining tenure.
- Preserving interest-saving and tenure-reduction information.
- Providing prepayment history.

---

# 8. Calculation Interfaces

Calculation modules are located in:

```text
src/calculations/
```

They are intentionally independent from Streamlit presentation code.

---

## `emi.py`

Provides EMI-related financial calculations.

The calculation layer is used by higher-level financial workflows rather than directly handling UI interaction.

---

## `amortization.py`

Provides amortization-related calculations, including repayment-period principal and interest allocation.

---

## `loan_analysis.py`

Provides remaining-loan analysis.

The service layer supplies:

```text
outstanding principal
annual interest rate
remaining tenure
```

The analysis returns information such as:

```text
EMI
remaining interest
remaining repayment
remaining principal
```

---

## `payment.py`

Provides payment-related financial calculations used by the payment workflow.

---

## `prepayment.py`

Provides prepayment analysis.

The prepayment calculation evaluates the effect of making an additional principal payment and produces information including:

```text
interest_saved
tenure_reduced_months
```

---

## `recommendations.py`

Provides the recommendation calculation.

## `recommend_prepayment_target(loans, prepayment_amount)`

### Inputs

```text
loans
prepayment_amount
```

### Validation

- At least one loan must be supplied.
- Prepayment amount must be greater than zero.

### Candidate processing

For each eligible loan:

1. Read outstanding principal.
2. Skip loans with no positive outstanding balance.
3. Limit the proposed prepayment to the outstanding principal when necessary.
4. Run prepayment analysis.
5. Build a recommendation candidate.

### Candidate fields

```text
loan_id
loan_name
interest_rate
prepayment_amount
interest_saved
tenure_reduced_months
```

### Ranking

Candidates are sorted by:

```text
interest_saved
```

in descending order.

The highest-interest-saving candidate becomes the recommendation.

---

# 9. Repository Interfaces

## Loan Repository

File:

```text
src/repositories/loan_repository.py
```

Core operations include:

```text
create_loan()
get_loan_by_id()
get_loans_by_user()
find_active_duplicate_loan()
archive_loan()
close_loan()
update_loan()
update_loan_balance()
```

These functions are responsible for database interaction rather than application-level validation.

---

## Payment Repository

File:

```text
src/repositories/payment_repository.py
```

Core operations include:

```text
create_payment()
get_payments_by_loan()
create_payment_and_update_loan()
create_prepayment_and_update_loan()
get_prepayments_by_loan()
```

The combined write operations use a database transaction.

---

# 10. Repository Transaction Pattern

Operations that create a financial activity and modify the loan state are grouped together.

For example:

```text
EMI Payment
    │
    ├── INSERT payment
    │
    └── UPDATE loan balance
```

and:

```text
Prepayment
    │
    ├── INSERT prepayment
    │
    └── UPDATE loan balance
```

Both are executed inside:

```python
with engine.begin() as connection:
```

This protects consistency between the activity history and current loan state.

---

# 11. Loan Status Operations

The application distinguishes between three important states:

```text
active
archived
closed
```

### Archive

```text
active → archived
```

The loan remains stored.

### Unarchive

```text
archived → active
```

The loan can be restored through the application's unarchive workflow.

### Close

```text
active → closed
```

Normal closing requires zero outstanding principal.

### Force Delete

Deletion is separate from the normal lifecycle:

```text
loan record → permanently removed
```

Force deletion is an explicit destructive management operation and is available for removing a loan record rather than preserving it through archive/close.

---

# 12. Error Handling Contract

Services use `ValueError` for expected validation and business-rule failures.

Typical errors include:

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
Remaining tenure cannot be negative.
Remaining tenure cannot exceed original tenure.
Outstanding principal cannot be negative.
Outstanding principal cannot exceed original principal.
Loan cannot be closed while outstanding principal exists.
Loan is already archived.
Loan is already closed.
Archived loans cannot be closed.
At least one loan is required.
Prepayment amount must be greater than zero.
No active loan is available for prepayment.
```

The Streamlit UI catches expected `ValueError` exceptions and presents them to the user.

---

# 13. Supported Loan Types

The service layer currently recognizes:

```text
home
car
personal
education
business
other
```

---

# 14. Supported Interest Types

The service layer currently recognizes:

```text
fixed
floating
```

---

# 15. Data Conversion

Database monetary values may be returned as database decimal types.

Service responses convert relevant monetary fields to Python `float` values before returning them to the application/UI.

This keeps the UI-facing service responses easier to consume.

---

# 16. Recommended Usage Pattern

Application code should generally follow:

```text
UI
 ↓
Service
 ↓
Repository / Calculation
```

Avoid putting raw SQL inside Streamlit UI code.

Avoid putting Streamlit-specific code inside calculation modules.

Avoid duplicating financial calculations in multiple layers.

For example:

```text
Correct:

Streamlit
   ↓
recommend_prepayment()
   ↓
recommend_prepayment_target()
   ↓
analyze_prepayment()
```

rather than implementing recommendation mathematics directly inside `app/main.py`.

---

# 17. Testing Contract

The current finalized project test suite reports:

```text
80 passed
```

When modifying service, repository, or calculation behavior, the full test suite should be executed before committing.

Expected successful result:

```text
80 passed
```

---

# 18. API Reference vs. UI

This document describes Python application interfaces, not HTTP REST endpoints.

LoanWise AI currently uses Streamlit as its application interface and does not require a separate REST API layer for its current architecture.

The functions documented here are therefore **internal application/service APIs** used by the Streamlit application and other Python components.

---

# 19. Extension Guidelines

When adding a new loan-management feature:

1. Add database access to the appropriate repository.
2. Add business validation/workflow to the appropriate service.
3. Add financial mathematics to `src/calculations/` when applicable.
4. Call the service from the Streamlit UI.
5. Add tests.
6. Update this reference when the public service interface changes.

This preserves the project's layered architecture.

---

# 20. Summary

The application-level dependency direction is:

```text
app/main.py
     ↓
services
     ↓
repositories
     ↓
database
```

and for financial operations:

```text
services
     ↓
calculations
```

The core design goal is to keep:

```text
Presentation
Business Logic
Persistence
Financial Mathematics
```

separated and independently testable.

