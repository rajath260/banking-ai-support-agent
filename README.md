# Banking AI Support Agent

An educational project for learning Python, LangGraph, Hugging Face, LLM tool calling, MCP and agent architecture through a fictional banking support use case.

> Safety: this project uses fictional in-memory data only. It is not connected to a bank or payment network. Never commit real customer data, credentials, tokens or account details.

## What you will learn
- Difference between an LLM, an agent and a workflow.
- Connecting a Python application to a hosted Hugging Face model.
- Function/tool calling: the model requests a tool; the application validates and executes it.
- LangGraph state, nodes, edges and conditional routing.
- MCP discovery and invocation through a standardized client/server protocol.
- Reliability concepts: validation, retries, checkpointing and human approval.

## Architecture

The project currently provides two runnable workflows:

1. **Basic deterministic workflow:** customer query -> keyword intent classification -> conditional route -> read-only mock banking function or general response.
2. **Hugging Face tool-calling agent:** customer query -> Hugging Face model -> optional approved tool call -> Python tool dispatcher -> model summarizes the tool result.

The LLM does not execute Python. It returns a structured tool request. The application validates the tool name and arguments, injects the account ID from application context, executes the allow-listed mock function and sends the result back to the model.

An MCP server exposes equivalent mock banking functions over stdio. An MCP client has not yet been connected.

## Structure
- app/state.py: state schema for the basic graph
- app/banking_tools.py: fictional read-only banking functions
- app/graph.py: original deterministic LangGraph workflow
- app/main.py: run the original deterministic workflow
- app/llm.py: Hugging Face hosted chat model connection
- app/agent_tools.py: model tool schemas and safe tool dispatcher
- app/agent_graph.py: LangGraph workflow with model tool calling
- app/agent_main.py: interactive entry point for the LLM agent
- mcp_server/server.py: MCP server exposing mock tools
- tests/test_graph.py: basic graph tests
- tests/test_agent_tools.py: tool allow-list and argument validation tests
- docs/concepts.md: interview-oriented explanations

## Setup
Python 3.11+ recommended.

Windows PowerShell:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configure Hugging Face
1. Create a Hugging Face access token with Inference Providers permission at https://huggingface.co/settings/tokens.
2. Create a local `.env` file in the repository root.
3. Add:
   ```env
   HF_TOKEN=hf_your_actual_token
   HF_MODEL=openai/gpt-oss-120b
   ```
4. Never commit `.env`; it is listed in `.gitignore`.

The default model is `openai/gpt-oss-120b`. Availability and tool-calling support depend on the selected inference provider and account.

## Run the Hugging Face connection
```powershell
python -m app.llm
```

## Run the LLM-powered banking agent
```powershell
python -m app.agent_main
```
Example prompts:
- What is my account balance?
- Show my last two transactions.
- Is my debit card active?
- What is the difference between a savings account and a current account?

The account ID is deliberately supplied by the application as `DEMO-001`. The model is not allowed to choose or override it.

## Run the original deterministic graph
```powershell
python -m app.main
```

## Run tests
```powershell
python -m pytest
```

Tests cover the deterministic graph and the banking tool dispatcher. They do not make a live Hugging Face API call.

## Run the MCP server
```powershell
python -m mcp_server.server
```
The MCP server uses stdio and is intended to be launched by an MCP host/client.

## Important concepts
| Concept | Meaning | Project example |
|---|---|---|
| LLM | Model that generates text from input | Hugging Face chat model |
| Tool schema | Description of a function the model may request | `BANKING_TOOLS` |
| Tool call | Structured request from the model | function name and JSON arguments |
| Tool dispatcher | Application code that validates and runs a tool | `execute_banking_tool` |
| Node | A unit of work in LangGraph | call model / execute tools / finish |
| Conditional edge | Chooses the next graph node | tool call or direct response |
| MCP | Standard protocol for tool/context exchange | mock banking MCP server |

## Banking security notes
A real banking application needs authentication, authorization at every tool boundary, consent and purpose checks, audit logs, encryption, secrets management, data minimization, rate limiting, monitoring, threat modelling and human approval for sensitive actions. This prototype is read-only and fictional.

## Learning milestones
1. Understand Python tools and LangGraph state/nodes/edges/reducers.
2. Connect a hosted Hugging Face model.
3. Let the model request approved banking tools through function calling (implemented in this milestone).
4. Connect an MCP client and discover/invoke tools.
5. Add conversation history, retries, robust error handling and tracing.
6. Add RAG for banking FAQs.
7. Prepare architecture diagrams and interview explanations.

## Interview summary
"I built a fictional banking support agent using LangGraph and a Hugging Face hosted model. The model can request approved read-only banking tools using structured function calling. The application validates the tool name and arguments, supplies trusted account context, executes the Python function and sends the result back to the model. LangGraph orchestrates the model and tool steps, while a separate MCP server demonstrates standardized tool exposure."
