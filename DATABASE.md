# LoanWise AI — Database Documentation

## Overview

LoanWise AI uses PostgreSQL as its persistent database.

The database stores loan profiles and financial activity associated with those loans.

## Core Loan Record

The `loans` table represents an individual loan belonging to a user.

Important fields include:

| Field | Purpose |
|---|---|
| `id` | Unique loan identifier |
| `user_id` | User who owns the loan |
| `loan_name` | User-facing loan name |
| `loan_type` | Loan category |
| `lender` | Financial institution/lender |
| `original_principal` | Original sanctioned/borrowed principal |
| `outstanding_principal` | Current outstanding principal |
| `interest_rate` | Interest rate |
| `interest_type` | Fixed or floating |
| `emi` | EMI amount |
| `original_tenure_months` | Original loan tenure |
| `remaining_tenure_months` | Current remaining tenure |
| `loan_start_date` | Loan start date |
| `emi_due_day` | Monthly EMI due day |
| `processing_charges` | Processing charges |
| `prepayment_rules` | Prepayment-related rules |
| `prepayment_charges` | Applicable prepayment charges |
| `status` | Current loan lifecycle state |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

## Loan Status

The application uses loan status values such as:

- `active`
- `archived`
- `closed`

Force deletion removes the record rather than assigning another status.

## Loan Payments

The `loan_payments` table stores EMI/payment activity.

The application uses fields including:

- payment ID
- loan ID
- payment date
- EMI amount
- principal component
- interest component
- outstanding balance
- late-payment indicator
- extra payment amount

This allows the application to build payment history and loan activity views.

## Prepayments

The `prepayments` table stores additional principal payments.

Relevant information includes:

- prepayment ID
- loan ID
- payment date
- amount
- principal before
- principal after
- interest saved
- tenure reduced
- strategy

This information supports prepayment analysis and activity history.

## Relationships

Conceptually:

```text
User
  │
  └──< Loans
          │
          ├──< Loan Payments
          │
          └──< Prepayments
```

A user can have multiple loans.

A loan can have multiple payment records and multiple prepayment records.

## Data Consistency

Operations that record a payment or prepayment and update the associated loan balance are performed transactionally by the repository layer.

This is important because the activity record and current loan balance should remain synchronized.

## Validation Rules

Loan creation validates rules including:

- user ID must be positive
- loan name cannot be empty
- lender cannot be empty
- loan type must be supported
- interest type must be supported
- original principal must be positive
- outstanding principal cannot be negative
- outstanding principal cannot exceed original principal
- interest rate cannot be negative
- EMI must be positive
- original tenure must be positive
- remaining tenure cannot be negative
- remaining tenure cannot exceed original tenure
- EMI due day, when supplied, must be between 1 and 31

## Duplicate Loan Protection

The application checks for an existing active loan with matching identifying characteristics before creating a new loan.

Archived loans do not participate in the active duplicate check.

## Database Access

Application code accesses PostgreSQL through the repository layer using SQLAlchemy.

The UI should not directly execute database queries.

## Backup and Reset

Before making structural database changes, create a database backup.

A clean database state can be used as a development checkpoint, while realistic demo data can be added through the application for testing the UI and workflows.
