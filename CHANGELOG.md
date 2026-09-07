# LoanWise AI — Changelog

All notable project milestones are recorded here.

## Finalized Project — September 2026

### Loan Management

- Added loan registration and validation.
- Added loan profile editing.
- Added support for loan types including:
  - home
  - car
  - personal
  - education
  - business
  - other
- Added fixed and floating interest-type support.
- Added duplicate active-loan protection.
- Added loan archiving.
- Added loan closing with validation.
- Added loan restoration/unarchive workflow.
- Added force-delete functionality for permanently removing unwanted loan records.

### Financial Analysis

- Added remaining-loan analysis.
- Added EMI and repayment calculations.
- Added amortization functionality.
- Added prepayment analysis.
- Added interest-savings calculations.
- Added tenure-reduction calculations.
- Added prepayment-target recommendations.

### Loan Activity

- Added EMI payment history.
- Added prepayment history.
- Added combined loan activity.
- Added activity summaries including principal, interest, extra payments, and outstanding balance.

### Database

- Added repository-based PostgreSQL access.
- Added transactional operations for payment/prepayment plus loan-balance updates.
- Added loan lifecycle status handling.

### Testing

The finalized checkpoint passes:

```text
80 passed
```

### Documentation

Documentation includes:

- `README.md`
- `API_REFERENCE.md`
- `ARCHITECTURE.md`
- `DATABASE.md`
- `DEVELOPMENT.md`
- `PROJECT_STRUCTURE.md`
- `CHANGELOG.md`

## Earlier Project Milestones

Earlier project work established the financial calculation foundation, database integration, loan-management services, Streamlit interface, and AI financial-advisor foundation.

Refer to Git history for the exact commit-by-commit development record:

```powershell
git log --oneline --decorate
```

## Git Checkpoints

The project has been maintained through Git checkpoints and pushed to the development branch.

Before future changes, preserve the current clean state with a commit and push.
