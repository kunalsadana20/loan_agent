from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from tools import calculate_emi, get_loan_details
from config import SYSTEM_PROMPT, LLM_MODEL
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END
import json

from langgraph.checkpoint.memory import InMemorySaver

tools_by_name = {t.name: t for t in [calculate_emi, get_loan_details]}
llm = ChatOllama(model=LLM_MODEL, temperature=0).bind_tools(list(tools_by_name.values()))
print("MODEL:", LLM_MODEL)

def llm_call(state: MessagesState):
    response = llm.invoke([SystemMessage(SYSTEM_PROMPT)] + state["messages"])
    return {"messages": [response]}

def tool_node(state: MessagesState):
    results = []
    for call in state["messages"][-1].tool_calls:
        try:
            result = tools_by_name[call["name"]].invoke(call["args"])
        except Exception as e:
            result = f"Error: {e}. Check the arguments and try again."

        content = result if isinstance(result, str) else json.dumps(result)
        results.append(ToolMessage(content=content, tool_call_id=call["id"]))
    return {"messages": results}

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    return "tool_node" if state["messages"][-1].tool_calls else END

builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")
# agent = builder.compile()

# result = agent.invoke({"messages": [HumanMessage("What is the EMI for loan LN001?")]})
# for m in result["messages"]:
#     m.pretty_print()



agent = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "customer-1"}}

for q in ["What is the EMI for loan LN001?", "Is that loan fully paid?"]:
    result = agent.invoke({"messages": [HumanMessage(q)]}, config)
    print("\nQ:", q)
    print("A:", result["messages"][-1].content)