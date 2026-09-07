import sys
from pathlib import Path

# Add project root (D:\LoanWise AI) to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from datetime import date

from src.services.user_service import (
    list_users,
)
from src.services.dashboard_service import get_dashboard_data

from src.services.loan_service import (
    register_loan,
    archive_user_loan,
    close_user_loan,
    update_loan_details,
    restore_user_loan,
    force_delete_user_loan,
)

from src.services.recommendation_service import (
    recommend_prepayment,
)

from src.services.payment_service import (
    record_loan_payment,
    get_loan_payment_history,
)

from src.services.prepayment_service import (
    record_loan_prepayment,
    get_loan_prepayment_history,
)

from src.calculations.loan_analysis import (
    analyze_remaining_loan,
)

from src.calculations.prepayment import (
    analyze_prepayment,
)

from src.services.loan_activity_service import (
    get_combined_loan_activity,
)

from src.utils.amount_words import amount_to_words

from src.services.ai_advisor_service import (
    build_ai_advisor_prompt,
)
from src.services.ai_provider_service import (
    generate_ai_response,
)

# ===================================================================
# PAGE CONFIGURATION
# ===================================================================

st.set_page_config(
    page_title="LoanWise AI",
    page_icon="💵",
    layout="wide",
)


st.title("LoanWise AI")
st.caption("Personal Loan & Debt Management")


# ===================================================================
# SIDEBAR - USER SELECTION
# ===================================================================

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
    st.sidebar.warning("No users found.")
    user_id = None


# ===================================================================
# ADD LOAN
# ===================================================================

st.header("Add Loan")

with st.form("add_loan_form"):

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------------
    # Loan Information
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
    # Repayment Information
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


# ===================================================================
# SAVE LOAN
# ===================================================================

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


# ===================================================================
# PORTFOLIO DASHBOARD
# ===================================================================

st.header("Portfolio Dashboard")

if user_id is not None:

    try:

        data = get_dashboard_data(user_id)

        portfolio = data["portfolio"]
        loans = data["loans"]

        # -----------------------------------------------------------
        # Portfolio Metrics
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
        # Loan Table
        # -----------------------------------------------------------

        st.subheader("Your Loans")

        if loans:

            st.dataframe(
                loans,
                width="stretch",
            )

            # =======================================================
            # LOAN ANALYSIS
            # =======================================================

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

                    col1, col2, col3, col4 = (
                        st.columns(4)
                    )

                    col1.metric(
                        "Outstanding",
                        f"Rs. {loan['outstanding_principal']:,.2f}",
                    )

                    col2.metric(
                        "Estimated Remaining Interest",
                        f"Rs. {analysis['remaining_interest']:,.2f}",
                    )

                    col3.metric(
                        "Remaining Repayment",
                        f"Rs. {analysis['remaining_repayment']:,.2f}",
                    )

                    col4.metric(
                        "Remaining Tenure",
                        f"{loan['remaining_tenure_months']} months",
                    )

            # =======================================================
            # MANAGE LOANS
            # =======================================================

            st.subheader("Manage Loans")

            loan_options = {
                f"{loan['loan_name']} - ID {loan['id']}":
                    loan["id"]
                for loan in loans
            }

            selected_loan_label = st.selectbox(
                "Select Loan",
                list(loan_options.keys()),
            )

            selected_loan_id = loan_options[
                selected_loan_label
            ]

            selected_loan = next(
                loan
                for loan in loans
                if loan["id"] == selected_loan_id
            )

            # =======================================================
            # ARCHIVE LOAN
            # =======================================================

            if st.button(
                "Archive Selected Loan",
                width="stretch",
            ):

                try:

                    archive_user_loan(
                        selected_loan_id
                    )

                    st.success(
                        "Loan archived successfully."
                    )

                    st.rerun()

                except ValueError as error:
                    st.error(str(error))

                except Exception as error:
                    st.error(
                        f"Unable to archive loan: {error}"
                    )

            # =======================================================
            # CLOSE LOAN
            # =======================================================

            if st.button(
                "Close Selected Loan",
                width="stretch",
            ):

                try:

                    close_user_loan(
                        selected_loan_id
                    )

                    st.success(
                        "Loan closed successfully."
                    )

                    st.rerun()

                except ValueError as error:
                    st.error(str(error))

                except Exception as error:
                    st.error(
                        f"Unable to close loan: {error}"
                    )

            # =======================================================
            # EDIT LOAN PROFILE
            # =======================================================

            st.subheader("Edit Loan Profile")

            with st.expander(
                "Edit Selected Loan"
            ):

                with st.form(
                    "edit_loan_form"
                ):

                    edit_col1, edit_col2 = (
                        st.columns(2)
                    )

                    with edit_col1:

                        edit_loan_name = (
                            st.text_input(
                                "Loan Name",
                                value=selected_loan[
                                    "loan_name"
                                ],
                            )
                        )

                        loan_types = [
                            "home",
                            "car",
                            "personal",
                            "education",
                            "business",
                            "other",
                        ]

                        current_loan_type = (
                            selected_loan[
                                "loan_type"
                            ]
                        )

                        if current_loan_type not in loan_types:
                            current_loan_type = "other"

                        edit_loan_type = (
                            st.selectbox(
                                "Loan Type",
                                loan_types,
                                index=loan_types.index(
                                    current_loan_type
                                ),
                            )
                        )

                        edit_lender = (
                            st.text_input(
                                "Lender",
                                value=selected_loan[
                                    "lender"
                                ],
                            )
                        )

                        interest_types = [
                            "fixed",
                            "floating",
                        ]

                        current_interest_type = (
                            selected_loan[
                                "interest_type"
                            ]
                        )

                        if (
                            current_interest_type
                            not in interest_types
                        ):
                            current_interest_type = "fixed"

                        edit_interest_type = (
                            st.selectbox(
                                "Interest Type",
                                interest_types,
                                index=interest_types.index(
                                    current_interest_type
                                ),
                            )
                        )

                        edit_interest_rate = (
                            st.number_input(
                                "Interest Rate (%)",
                                min_value=0.0,
                                value=float(
                                    selected_loan[
                                        "interest_rate"
                                    ]
                                ),
                                step=0.1,
                            )
                        )

                    with edit_col2:

                        edit_emi = (
                            st.number_input(
                                "EMI",
                                min_value=0.0,
                                value=float(
                                    selected_loan[
                                        "emi"
                                    ]
                                ),
                                step=100.0,
                            )
                        )

                        edit_original_tenure = (
                            st.number_input(
                                "Original Tenure (Months)",
                                min_value=1,
                                value=int(
                                    selected_loan[
                                        "original_tenure_months"
                                    ]
                                ),
                                step=1,
                            )
                        )

                        edit_start_date = (
                            st.date_input(
                                "Loan Start Date",
                                value=selected_loan[
                                    "loan_start_date"
                                ],
                            )
                        )

                        current_due_day = (
                            selected_loan[
                                "emi_due_day"
                            ]
                        )

                        if current_due_day is None:
                            current_due_day = 5

                        edit_due_day = (
                            st.number_input(
                                "EMI Due Day",
                                min_value=1,
                                max_value=31,
                                value=int(
                                    current_due_day
                                ),
                                step=1,
                            )
                        )

                        edit_processing_charges = (
                            st.number_input(
                                "Processing Charges",
                                min_value=0.0,
                                value=float(
                                    selected_loan[
                                        "processing_charges"
                                    ]
                                ),
                                step=100.0,
                            )
                        )

                    edit_prepayment_rules = (
                        st.text_input(
                            "Prepayment Rules",
                            value=(
                                selected_loan[
                                    "prepayment_rules"
                                ]
                                or ""
                            ),
                        )
                    )

                    edit_prepayment_charges = (
                        st.number_input(
                            "Prepayment Charges",
                            min_value=0.0,
                            value=float(
                                selected_loan[
                                    "prepayment_charges"
                                ]
                            ),
                            step=100.0,
                        )
                    )

                    save_changes = (
                        st.form_submit_button(
                            "Save Changes",
                            width="stretch",
                        )
                    )

                if save_changes:

                    try:

                        update_loan_details(
                            loan_id=selected_loan_id,
                            loan_name=edit_loan_name,
                            loan_type=edit_loan_type,
                            lender=edit_lender,
                            interest_rate=edit_interest_rate,
                            interest_type=edit_interest_type,
                            emi=edit_emi,
                            original_tenure_months=(
                                edit_original_tenure
                            ),
                            loan_start_date=edit_start_date,
                            emi_due_day=edit_due_day,
                            processing_charges=(
                                edit_processing_charges
                            ),
                            prepayment_rules=(
                                edit_prepayment_rules
                                or None
                            ),
                            prepayment_charges=(
                                edit_prepayment_charges
                            ),
                        )

                        st.success(
                            "Loan profile updated successfully."
                        )

                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))

                    except Exception as error:
                        st.error(
                            f"Unable to update loan: {error}"
                        )

            # =======================================================
            # RECORD EMI PAYMENT
            # =======================================================

            st.subheader(
                "Record EMI Payment"
            )

            with st.expander(
                "Record Payment"
            ):

                payment_date = st.date_input(
                    "Payment Date",
                    value=date.today(),
                )

                extra_payment = st.number_input(
                    "Extra Payment",
                    min_value=0.0,
                    step=1000.0,
                )

                if extra_payment > 0:

                    st.caption(
                        amount_to_words(
                            extra_payment
                        )
                    )

                late_payment = st.checkbox(
                    "Late Payment"
                )

                if st.button(
                    "Record EMI Payment",
                    width="stretch",
                ):

                    try:

                        result = record_loan_payment(
                            loan_id=selected_loan_id,
                            payment_date=payment_date,
                            extra_payment=extra_payment,
                            late_payment=late_payment,
                        )

                        calculation = result[
                            "calculation"
                        ]

                        st.success(
                            "EMI payment recorded successfully."
                        )

                        col1, col2, col3 = (
                            st.columns(3)
                        )

                        col1.metric(
                            "Interest",
                            f"Rs. {calculation['interest_component']:,.2f}",
                        )

                        col2.metric(
                            "Principal Paid",
                            f"Rs. {calculation['principal_component']:,.2f}",
                        )

                        col3.metric(
                            "New Outstanding",
                            f"Rs. {calculation['outstanding_balance']:,.2f}",
                        )

                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))

                    except Exception as error:
                        st.error(
                            f"Unable to record payment: {error}"
                        )

            # =======================================================
            # PAYMENT HISTORY
            # =======================================================

            st.subheader(
                "Payment History"
            )

            try:

                payments = (
                    get_loan_payment_history(
                        selected_loan_id
                    )
                )

                if payments:

                    st.dataframe(
                        payments,
                        width="stretch",
                    )

                else:

                    st.info(
                        "No payments recorded yet."
                    )

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(
                    f"Unable to load payment history: {error}"
                )

            # =======================================================
            # RECORD PREPAYMENT
            # =======================================================

            st.subheader(
                "Record Prepayment"
            )

            outstanding_balance = float(
                selected_loan[
                    "outstanding_principal"
                ]
            )

            with st.expander(
                "Record Prepayment"
            ):

                st.metric(
                    "Current Outstanding",
                    f"Rs. {outstanding_balance:,.2f}",
                )

                st.caption(
                    "You can prepay any amount up to the current "
                    "outstanding principal."
                )

                prepayment_date = st.date_input(
                    "Prepayment Date",
                    value=date.today(),
                    key="prepayment_date",
                )

                prepayment_amount = st.number_input(
                    "Prepayment Amount",
                    min_value=0.0,
                    max_value=outstanding_balance,
                    step=1000.0,
                    value=0.0,
                    key="prepayment_amount",
                )

                if prepayment_amount > 0:

                    st.caption(
                        amount_to_words(
                            prepayment_amount
                        )
                    )

                    # ------------------------------------------------
                    # PREPAYMENT PREVIEW
                    # ------------------------------------------------

                    try:

                        preview = analyze_prepayment(
                            outstanding_principal=(
                                outstanding_balance
                            ),
                            annual_interest_rate=float(
                                selected_loan[
                                    "interest_rate"
                                ]
                            ),
                            remaining_tenure_months=int(
                                selected_loan[
                                    "remaining_tenure_months"
                                ]
                            ),
                            prepayment_amount=(
                                prepayment_amount
                            ),
                        )

                        st.divider()

                        st.subheader(
                            "Prepayment Impact"
                        )

                        col1, col2, col3 = (
                            st.columns(3)
                        )

                        col1.metric(
                            "Amount",
                            f"Rs. {prepayment_amount:,.2f}",
                        )

                        col2.metric(
                            "Interest Saved",
                            f"Rs. {preview['interest_saved']:,.2f}",
                        )

                        col3.metric(
                            "New Outstanding",
                            f"Rs. {preview['principal_after']:,.2f}",
                        )

                        st.info(
                            f"Estimated tenure reduction: "
                            f"{preview['tenure_reduced_months']} months"
                        )

                    except ValueError as error:
                        st.error(str(error))

                    except Exception as error:
                        st.error(
                            f"Unable to calculate prepayment impact: {error}"
                        )

                st.divider()

                if st.button(
                    "Record Prepayment",
                    key="record_prepayment",
                    width="stretch",
                    disabled=prepayment_amount <= 0,
                ):

                    try:

                        result = record_loan_prepayment(
                            loan_id=selected_loan_id,
                            payment_date=prepayment_date,
                            prepayment_amount=prepayment_amount,
                        )

                        analysis = result[
                            "analysis"
                        ]

                        st.success(
                            "Prepayment recorded successfully."
                        )

                        col1, col2, col3 = (
                            st.columns(3)
                        )

                        col1.metric(
                            "Principal Before",
                            f"Rs. {analysis['principal_before']:,.2f}",
                        )

                        col2.metric(
                            "Principal After",
                            f"Rs. {analysis['principal_after']:,.2f}",
                        )

                        col3.metric(
                            "Interest Saved",
                            f"Rs. {analysis['interest_saved']:,.2f}",
                        )

                        st.info(
                            f"Tenure reduction: "
                            f"{analysis['tenure_reduced_months']} months"
                        )

                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))

                    except Exception as error:
                        st.error(
                            f"Unable to record prepayment: {error}"
                        )

            # =======================================================
            # COMBINED LOAN ACTIVITY
            # =======================================================

            st.subheader(
                "Loan Activity"
            )

            try:

                activities = (
                    get_combined_loan_activity(
                        selected_loan_id
                    )
                )

                if activities:

                    activity_rows = []

                    for activity in activities:

                        activity_rows.append(
                            {
                                "Date": activity[
                                    "date"
                                ],
                                "Type": activity[
                                    "type"
                                ],
                                "Amount": (
                                    f"Rs. "
                                    f"{activity['amount']:,.2f}"
                                ),
                                "Principal Paid": (
                                    f"Rs. "
                                    f"{activity['principal_paid']:,.2f}"
                                ),
                                "Interest Paid": (
                                    f"Rs. "
                                    f"{activity['interest_paid']:,.2f}"
                                ),
                                "Extra Payment": (
                                    f"Rs. "
                                    f"{activity['extra_payment']:,.2f}"
                                ),
                                "Interest Saved": (
                                    f"Rs. "
                                    f"{activity['interest_saved']:,.2f}"
                                ),
                                "Outstanding Balance": (
                                    f"Rs. "
                                    f"{activity['outstanding_balance']:,.2f}"
                                ),
                                "Tenure Reduced": (
                                    f"{activity['tenure_reduced_months']} months"
                                ),
                                "Late Payment": (
                                    "Yes"
                                    if activity[
                                        "late_payment"
                                    ]
                                    else "No"
                                ),
                            }
                        )

                    st.dataframe(
                        activity_rows,
                        width="stretch",
                        hide_index=True,
                    )

                else:

                    st.info(
                        "No loan activity recorded yet."
                    )

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(
                    f"Unable to load loan activity: {error}"
                )

            # =======================================================
            # PREPAYMENT HISTORY
            # =======================================================

            st.subheader(
                "Prepayment History"
            )

            try:

                prepayments = (
                    get_loan_prepayment_history(
                        selected_loan_id
                    )
                )

                if prepayments:

                    st.dataframe(
                        prepayments,
                        width="stretch",
                    )

                else:

                    st.info(
                        "No prepayments recorded yet."
                    )

            except ValueError as error:
                st.error(
                    f"Unable to load prepayment history: {error}"
                )

            except Exception as error:
                st.error(
                    f"Unable to load prepayment history: {error}"
                )

        else:

            st.info(
                "No loans found for this user."
            )

    except Exception as error:

        st.error(
            f"Unable to load dashboard: {error}"
        )


# ===================================================================
# PREPAYMENT RECOMMENDATION
# ===================================================================

st.header(
    "Prepayment Recommendation"
)

if user_id is not None:

    recommendation_amount = st.number_input(
        "Available Prepayment Amount",
        min_value=0.0,
        step=1000.0,
        value=0.0,
        key="recommendation_prepayment_amount",
    )

    if recommendation_amount > 0:

        st.caption(
            amount_to_words(
                recommendation_amount
            )
        )

    if st.button(
        "Analyze Prepayment",
        width="stretch",
    ):

        try:

            recommendation = recommend_prepayment(
                user_id=user_id,
                prepayment_amount=recommendation_amount,
            )

            recommended_loan = (
                recommendation[
                    "recommended_loan"
                ]
            )

            st.success(
                "Recommended loan for prepayment:"
            )

            st.subheader(
                recommended_loan[
                    "loan_name"
                ]
            )

            col1, col2, col3 = (
                st.columns(3)
            )

            col1.metric(
                "Interest Rate",
                f"{recommended_loan['interest_rate']:.2f}%",
            )

            col2.metric(
                "Interest Saved",
                f"Rs. {recommended_loan['interest_saved']:,.2f}",
            )

            col3.metric(
                "Tenure Reduced",
                f"{recommended_loan['tenure_reduced_months']} months",
            )

            # -------------------------------------------------------
            # PREPAYMENT COMPARISON
            # -------------------------------------------------------

            st.subheader(
                "Prepayment Comparison"
            )

            comparison = [
                {
                    "Loan": candidate[
                        "loan_name"
                    ],
                    "Interest Rate": (
                        f"{candidate['interest_rate']:.2f}%"
                    ),
                    "Prepayment": (
                        f"Rs. "
                        f"{candidate['prepayment_amount']:,.2f}"
                    ),
                    "Interest Saved": (
                        f"Rs. "
                        f"{candidate['interest_saved']:,.2f}"
                    ),
                    "Tenure Reduced": (
                        f"{candidate['tenure_reduced_months']} months"
                    ),
                }
                for candidate in recommendation[
                    "candidates"
                ]
            ]

            st.dataframe(
                comparison,
                width="stretch",
                hide_index=True,
            )

        except ValueError as error:

            st.error(
                str(error)
            )

        except Exception as error:

            st.error(
                f"Unable to analyze prepayment: {error}"
            )
# ===================================================================
# AI FINANCIAL ADVISOR
# ===================================================================

st.header("🤖 AI Financial Advisor")

if user_id is not None:

    st.caption(
        "Ask questions about your loans, repayment strategy, "
        "prepayment, interest costs, or debt management."
    )

    ai_question = st.text_area(
        "Ask LoanWise AI",
        placeholder=(
            "Example: Which loan should I prioritize "
            "for prepayment?"
        ),
        height=100,
        key="ai_question",
    )

    if st.button(
        "Ask AI",
        width="stretch",
        key="ask_ai",
    ):

        if not ai_question or not ai_question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "LoanWise AI is analyzing your financial data..."
                ):

                    prompt = build_ai_advisor_prompt(
                        user_id=user_id,
                        question=ai_question,
                    )

                    answer = generate_ai_response(
                        prompt
                    )

                st.subheader(
                    "LoanWise AI"
                )

                st.write(answer)

            except ValueError as error:

                st.error(
                    str(error)
                )

            except Exception as error:

                st.error(
                    f"Unable to generate AI response: {error}"
                )

else:

    st.info(
        "Select a user to use the AI Financial Advisor."
    )