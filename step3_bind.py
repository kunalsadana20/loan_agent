from langchain_ollama import ChatOllama
from tools import calculate_emi, get_loan_details

llm = ChatOllama(model="llama3.2:3b", temperature=0)
llm_with_tools = llm.bind_tools([calculate_emi, get_loan_details])

questions = [
    "What's the EMI on ₹5 lakh at 12% for 3 years?",
    "What is the status of loan LN002?",
    "What is the EMI for loan LN001?",
    "What is an EMI?",
]

for q in questions:
    response = llm_with_tools.invoke(q)
    print("\nQ:", q)
    print("content:", repr(response.content))
    print("tool_calls:", response.tool_calls)
    print("input_tokens:", response.usage_metadata["input_tokens"])