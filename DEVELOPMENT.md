# LoanWise AI — Development Guide

## Prerequisites

Recommended environment:

- Python 3.x
- PostgreSQL
- Git
- PowerShell on Windows

## Virtual Environment

From the project directory:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

Install the project's dependencies using the project's dependency file if present.

Typical command:

```powershell
pip install -r requirements.txt
```

## Running the Application

Launch the Streamlit application from the project root:

```powershell
streamlit run app/main.py
```

## Running Tests

Run the complete test suite:

```powershell
pytest
```

The finalized checkpoint currently has:

```text
80 passed
```

## Development Workflow

A practical workflow is:

```text
1. Make a focused change
2. Run relevant tests
3. Run the complete test suite
4. Inspect git diff
5. Check git status
6. Commit
7. Push
```

Useful commands:

```powershell
git status
git diff
git add .
git commit -m "description"
git push origin database
```

## PowerShell Notes

For a clean status check:

```powershell
git status
```

For a concise recent history:

```powershell
git log --oneline -5
```

To inspect a specific file:

```powershell
Get-Content .\path	oile.py
```

or:

```powershell
type .\path	oile.py
```

## Validation Before Commit

Before committing application changes:

```powershell
pytest
git status
git diff
```

Do not commit generated secrets, database credentials, virtual environments, or local-only configuration.

## Service-Layer Changes

When adding a new loan operation:

1. Define or update repository functionality.
2. Add service-level validation.
3. Keep financial calculations in the calculations layer.
4. Connect the operation to the Streamlit UI.
5. Add or update tests.
6. Run the complete test suite.

## Database Changes

For database schema changes:

1. Back up the database.
2. Make the smallest necessary schema change.
3. Verify existing functionality.
4. Run tests.
5. Test the relevant UI workflow.
6. Commit the schema/application changes together when appropriate.

## Destructive Operations

Force deletion is a destructive operation.

Use it only when the loan should be permanently removed rather than archived.

Before destructive database work, create a backup.

## Documentation Workflow

Documentation files should remain synchronized with the implemented application.

Current documentation set:

- `README.md`
- `API_REFERENCE.md`
- `ARCHITECTURE.md`
- `DATABASE.md`
- `DEVELOPMENT.md`
- `PROJECT_STRUCTURE.md`
- `CHANGELOG.md`

## Release Check

Before considering a project checkpoint complete:

```powershell
pytest
git status
git log --oneline -5
```

The working tree should be clean and the latest documentation/application changes should be pushed to the intended branch.
