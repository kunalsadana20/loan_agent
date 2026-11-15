from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from tools import calculate_emi, get_loan_details
from config import SYSTEM_PROMPT, LLM_MODEL
import json

tools_by_name = {t.name: t for t in [calculate_emi, get_loan_details]}
llm = ChatOllama(model=LLM_MODEL, temperature=0).bind_tools(list(tools_by_name.values()))
print("MODEL:", LLM_MODEL)

question = "What is the EMI for loan LN003?"


def run_agent(question, max_steps=5):
    messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(question)]

    for step in range(max_steps):
        ai_msg = llm.invoke(messages)               # call the model with the whole list
        messages.append(ai_msg)

        if not ai_msg.tool_calls:                   # the model asked for no tools
            return ai_msg.content, messages

        for call in ai_msg.tool_calls:
            print("CALL:", call["name"], call["args"])
            try:
                result = tools_by_name[call["name"]].invoke(call["args"])
            except Exception as e:
                result = f"Error: {e}. Check the arguments and try again."

            content = result if isinstance(result, str) else json.dumps(result)
            messages.append(ToolMessage(content=content, tool_call_id=call["id"]))  
            # your existing lines: print CALL, try/except, json content, ToolMessage

    return "Stopped: reached max_steps", messages


# tests = [
#     ("What is the EMI for loan LN003?", "9,025.83"),
#     ("What is the EMI for loan LN001?", "3,445.06"),
# ]

# for question, expected in tests:
#     passed = 0
#     for i in range(5):
#         answer, msgs = run_agent(question)
#         passed += expected in answer
#         if expected not in answer:
#             print("  FAIL:", answer[:150])
#     print(f"{question} -> {passed}/5")


edge_tests = [
    "What is an EMI?",
    "What is the EMI for loan LN004?",
    "What's the EMI on ₹5 lakh at 12% for 3 years?",
]

for question in edge_tests:
    print("\nQ:", question)
    answer, msgs = run_agent(question)
    print("A:", answer)