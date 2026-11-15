# Loan Assistant Agent

A small learning project: a tool-calling agent that answers loan questions, built three ways to understand how agents work. It runs fully locally with Ollama.

The loan data is made up. Nothing here is production code.

## What it does

The agent has two tools:

- `calculate_emi(principal, annual_rate_pct, tenure_months)` computes a monthly EMI.
- `get_loan_details(loan_id)` looks up a loan in a small dummy dataset.

Asked "What is the EMI for loan LN001?", it looks up the loan, passes the values to the calculator and answers with the result.

## Three builds

| File | Approach |
| --- | --- |
| `step4_manual.py` | Agent loop written by hand: call the model, run requested tools, feed results back, repeat |
| `step5_graph.py` | The same loop as a LangGraph `StateGraph`, with a checkpointer for multi-turn memory |
| `step6_prebuilt.py` | LangChain's prebuilt `create_agent` |

Earlier steps (`step1_hello.py` to `step3_bind.py`) cover the first model call, the tools, and inspecting a raw tool call.

## Findings

I tested a two-step question (look up a loan, then calculate its EMI) on three local models, with the same code and prompt.

| Model | Runs passed |
| --- | --- |
| llama3.2:3b | 0 of 10 |
| qwen2.5:3b | 1 of 20 |
| qwen3:4b | 10 of 10 |

The sample is small and the pass check is a string match, so treat these as indications.

Failures seen on the 3B models:

- Calling a tool when none was needed
- Skipping the tool and doing the arithmetic itself, incorrectly
- Calling a tool with empty arguments
- Writing the tool call as plain text, so it was never parsed
- Rejecting valid tool data (a 3-month tenure) as an error

What helped: returning JSON from tools, sending tool errors back to the model so the loop survives, and a stronger model. Prompt rules helped little, and one rule introduced a new failure.

## Setup

Requires Python 3.12 and [Ollama](https://ollama.com).

```powershell
ollama pull qwen3:4b
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python step5_graph.py
```

The model name and system prompt are set in `config.py`.

## Not done yet

- Connecting a document retriever as a third tool (agentic RAG)
- Multi-agent workflows
- A larger evaluation set
