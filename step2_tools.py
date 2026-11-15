from tools import calculate_emi
from tools import get_loan_details


print(get_loan_details.name)
print(get_loan_details.description)
print(get_loan_details.args)

for lid in ["LN001","LN002","LN003","LN004"]:
    loan_det = get_loan_details.invoke({"loan_id": lid})
    if "error" in loan_det:
        print(loan_det)
        continue
    name = loan_det["name"]
    principal = loan_det["principal"]
    rate = loan_det["annual_rate_pct"]
    tenure = loan_det["tenure_months"]
    # print(calculate_emi.name)
    # print(calculate_emi.description)
    # print(calculate_emi.args)
    print(loan_det)
    print(calculate_emi.invoke({"principal": principal, "annual_rate_pct": rate, "tenure_months": tenure}))