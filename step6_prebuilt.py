from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from tools import calculate_emi, get_loan_details
from config import SYSTEM_PROMPT, LLM_MODEL

llm = ChatOllama(model=LLM_MODEL, temperature=0)

agent = create_agent(
    model=llm,
    tools=[calculate_emi, get_loan_details],
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke({"messages": [HumanMessage("What is the EMI for loan LN001?")]})
for m in result["messages"]:
    m.pretty_print()