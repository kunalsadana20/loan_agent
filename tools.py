from langchain_core.tools import tool

@tool(parse_docstring=True)
def calculate_emi(principal: float, annual_rate_pct: float, tenure_months: int) -> float:
    """Calculate the monthly EMI for a loan.

    Args:
        principal: Loan amount in rupees.
        annual_rate_pct: Annual interest rate in percent, e.g. 12 for 12%.
        tenure_months: Loan tenure in months.
    """
    r = annual_rate_pct / 12 / 100
    factor = (1 + r) ** tenure_months
    return round(principal * r * factor / (factor - 1), 2)



loans = {
    "LN001": {"loan_id":"LN001","name":"Akshay","principal":10000,"annual_rate_pct":20,"tenure_months":3,"status":"unpaid"},
    "LN002": {"loan_id":"LN002","name":"Aakash","principal":50000,"annual_rate_pct":18,"tenure_months":9,"status":"paid"},
    "LN003": {"loan_id":"LN003","name":"Avinash","principal":100000,"annual_rate_pct":15,"tenure_months":12,"status":"partially_paid"}
}


@tool(parse_docstring=True)
def get_loan_details(loan_id: str) -> dict:
    """Look up the details of an existing loan by its loan ID.

    Use this when the user asks about a specific loan, for example its
    amount, interest rate, tenure or repayment status. Returns the customer
    name, principal in rupees, annual interest rate in percent, tenure in
    months and status. If the ID does not exist, returns an error message.

    Args:
        loan_id: Loan ID in the format LN001.
    """
    if loan_id in loans.keys():
        return loans[loan_id]
    else:
        return {"error": f"No loan found with ID {loan_id}"}

