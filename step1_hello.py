from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b", temperature=0)

messages = [
    ("system", "You are a loan assistant. Answer in one sentence."),
    ("human", "What's the EMI on ₹5 lakh at 12% for 3 years?"),
]

response = llm.invoke(messages)

print(type(response))
print(response.content)
print(response.tool_calls)
print(response.usage_metadata)