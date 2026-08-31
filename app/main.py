import streamlit as st
from datetime import date

from src.services.dashboard_service import get_dashboard_data
from src.services.loan_service import register_loan
from src.services.user_service import list_users

from src.utils.amount_words import amount_to_words

from src.calculations.loan_analysis import (
    analyze_remaining_loan,
)


st.set_page_config(
    page_title="LoanWise AI",
    page_icon="Loan",
    layout="wide",
)


st.title("LoanWise AI")
st.caption("Personal Loan & Debt Management")


# -------------------------------------------------------------------
# Sidebar - User
# -------------------------------------------------------------------

st.sidebar.header("User")

users = list_users()

if users:
    user_options = {
        f"{user['name']} ({user['email']})": user["id"]
        for user in users
    }

    selected_user = st.sidebar.selectbox(
        "Select User",
        list(user_options.keys()),
    )

    user_id = user_options[selected_user]

else:
    st.sidebar.warning(
        "No users found."
    )

    user_id = None


# -------------------------------------------------------------------
# Add Loan
# -------------------------------------------------------------------

st.header("Add Loan")

with st.form("add_loan_form"):
    col1, col2 = st.columns(2)

    # ---------------------------------------------------------------
    # Left column
    # ---------------------------------------------------------------

    with col1:
        loan_name = st.text_input(
            "Loan Name",
            placeholder="e.g. Car Loan",
        )

        loan_type = st.selectbox(
            "Loan Type",
            [
                "home",
                "car",
                "personal",
                "education",
                "business",
                "other",
            ],
        )

        lender = st.text_input(
            "Lender",
            placeholder="e.g. HDFC Bank",
        )

        original_principal = st.number_input(
            "Original Principal",
            min_value=0.0,
            step=1000.0,
        )

        if original_principal > 0:
            st.caption(
                amount_to_words(original_principal)
            )

        outstanding_principal = st.number_input(
            "Outstanding Principal",
            min_value=0.0,
            step=1000.0,
        )

        if outstanding_principal > 0:
            st.caption(
                amount_to_words(outstanding_principal)
            )

        interest_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            step=0.1,
        )

        interest_type = st.selectbox(
            "Interest Type",
            [
                "fixed",
                "floating",
            ],
        )

    # ---------------------------------------------------------------
    # Right column
    # ---------------------------------------------------------------

    with col2:
        emi = st.number_input(
            "EMI",
            min_value=0.0,
            step=100.0,
        )

        if emi > 0:
            st.caption(
                amount_to_words(emi)
            )

        original_tenure_months = st.number_input(
            "Original Tenure (Months)",
            min_value=1,
            step=1,
        )

        remaining_tenure_months = st.number_input(
            "Remaining Tenure (Months)",
            min_value=0,
            step=1,
        )

        loan_start_date = st.date_input(
            "Loan Start Date",
            value=date.today(),
        )

        emi_due_day = st.number_input(
            "EMI Due Day",
            min_value=1,
            max_value=31,
            value=5,
            step=1,
        )

        processing_charges = st.number_input(
            "Processing Charges",
            min_value=0.0,
            step=100.0,
        )

        prepayment_charges = st.number_input(
            "Prepayment Charges",
            min_value=0.0,
            step=100.0,
        )

        prepayment_rules = st.text_input(
            "Prepayment Rules",
            placeholder="Optional",
        )

    submitted = st.form_submit_button(
        "Add Loan",
        width="stretch",
    )


# -------------------------------------------------------------------
# Save Loan
# -------------------------------------------------------------------

if submitted and user_id is not None:
    try:
        loan = register_loan(
            user_id=user_id,
            loan_name=loan_name,
            loan_type=loan_type,
            lender=lender,
            original_principal=original_principal,
            outstanding_principal=outstanding_principal,
            interest_rate=interest_rate,
            interest_type=interest_type,
            emi=emi,
            original_tenure_months=original_tenure_months,
            remaining_tenure_months=remaining_tenure_months,
            loan_start_date=loan_start_date,
            emi_due_day=emi_due_day,
            processing_charges=processing_charges,
            prepayment_rules=prepayment_rules or None,
            prepayment_charges=prepayment_charges,
        )

        st.success(
            f"Loan '{loan['loan_name']}' added successfully."
        )

        st.rerun()

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(
            f"Unable to add loan: {error}"
        )


# -------------------------------------------------------------------
# Portfolio Dashboard
# -------------------------------------------------------------------

st.header("Portfolio Dashboard")

if user_id is not None:
    try:
        data = get_dashboard_data(user_id)

        portfolio = data["portfolio"]
        loans = data["loans"]

        # -----------------------------------------------------------
        # Portfolio metrics
        # -----------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Loans",
            portfolio["loan_count"],
        )

        col2.metric(
            "Outstanding Principal",
            f"Rs. {portfolio['total_outstanding_principal']:,.2f}",
        )

        col3.metric(
            "Total EMI",
            f"Rs. {portfolio['total_emi']:,.2f}",
        )

        col4.metric(
            "Weighted Interest Rate",
            f"{portfolio['weighted_interest_rate']:.2f}%",
        )

        # -----------------------------------------------------------
        # Loan table
        # -----------------------------------------------------------

        st.subheader("Your Loans")

        if loans:
            st.dataframe(
                loans,
                width="stretch",
            )

            # -------------------------------------------------------
            # Loan analysis
            # -------------------------------------------------------

            st.subheader("Loan Analysis")

            for loan in loans:
                analysis = analyze_remaining_loan(
                    outstanding_principal=loan[
                        "outstanding_principal"
                    ],
                    annual_interest_rate=loan[
                        "interest_rate"
                    ],
                    remaining_tenure_months=loan[
                        "remaining_tenure_months"
                    ],
                )

                with st.expander(
                    loan["loan_name"]
                ):
                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Outstanding",
                        f"Rs. {loan['outstanding_principal']:,.2f}",
                    )

                    col2.metric(
                        "Estimated Remaining Interest",
                        f"Rs. {analysis['remaining_interest']:,.2f}",
                    )

                    col3.metric(
                        "Remaining Tenure",
                        f"{loan['remaining_tenure_months']} months",
                    )

        else:
            st.info(
                "No loans found for this user."
            )

    except Exception as error:
        st.error(
            f"Unable to load dashboard: {error}"
        )