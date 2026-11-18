# Banking AI Support Agent

An educational project for learning Python, LangGraph, LangChain, Hugging Face, MCP and LLM tool calling through a fictional banking support use case.

> Safety: this project uses fictional in-memory data only. It is not connected to a bank or payment network. Never commit real customer data, credentials, tokens or account details.

## What you will learn
- Difference between an LLM, an agent and a workflow.
- Connecting a Python application to a hosted Hugging Face model.
- Tool calling: the model requests a tool; the application validates and executes it.
- MCP: standardized discovery and invocation of tools through a client/server protocol.
- LangGraph: StateGraph, state, nodes, edges, conditional routing and reducers.
- Reliability concepts to add later: validation, retries, checkpointing and human approval.

## Architecture today
The project currently contains two separate paths:

1. **Existing deterministic LangGraph workflow:** customer query -> keyword intent classification -> conditional route -> read-only mock banking function or general response.
2. **New Hugging Face connection:** Python prompt -> Hugging Face Inference Providers -> model response.

The Hugging Face connection is an LLM call, not yet an integrated agent. It does not currently select or execute banking tools. We will connect model tool calling to LangGraph in a later milestone.

An MCP server exposes equivalent mock banking functions over stdio. An MCP client has not yet been connected.

## Structure
- app/state.py: shared graph state and reducer example
- app/banking_tools.py: fictional read-only banking functions
- app/graph.py: LangGraph nodes, edges and conditional routing
- app/main.py: runnable graph examples
- app/llm.py: Hugging Face hosted chat model connection
- mcp_server/server.py: MCP server exposing mock tools
- tests/test_graph.py: basic graph tests
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
1. Create or sign in to a Hugging Face account.
2. Create a user access token with **Inference Providers** permission at https://huggingface.co/settings/tokens.
3. Create a file named `.env` in the repository root (next to `.env.example`).
4. Add your token:
   ```env
   HF_TOKEN=hf_your_actual_token
   HF_MODEL=openai/gpt-oss-120b
   ```
5. Keep `.env` private. It is listed in `.gitignore`; never commit it.

The default model is `openai/gpt-oss-120b`. You can override it with `HF_MODEL` if another chat model is available to your Hugging Face account through Inference Providers. Availability, provider support and pricing can change.

Run the Hugging Face connection from the repository root:
```powershell
python -m app.llm
```

Run the existing deterministic graph:
```powershell
python -m app.main
```

Run tests:
```powershell
python -m pytest
```

Run the MCP server:
```powershell
python -m mcp_server.server
```

The MCP server uses stdio. It is intended to be launched by an MCP host/client, not used as a normal interactive terminal command.

## Key concepts
| Concept | Meaning | Project example |
|---|---|---|
| LLM | Model that generates text from input | Hugging Face chat model in app/llm.py |
| State | Shared data passed between graph nodes | query, intent, result |
| Node | A unit of work | classify request |
| Edge | Fixed transition | tool node to response node |
| Conditional edge | Chooses next node | tool path or general path |
| Reducer | Defines how updates to a state key merge | append execution trace |
| START / END | Graph entry and termination markers | graph boundaries |

## Tool calling vs MCP
Tool calling is a model/application interaction pattern: the model emits a structured request naming a tool and its arguments. The application validates, authorizes and executes it, then returns the result to the model. The model does not execute Python or directly access a database.

MCP is a protocol for discovering and invoking tools and other context across a standardized client/server boundary. An MCP host can discover server tools and make them available to a model. The model may request a tool call; the host/client performs the MCP invocation.

LangGraph orchestrates the application workflow. MCP does not replace the model, tool calling or authorization logic.

## Banking security notes
A real banking application needs authentication, authorization at every tool boundary, consent and purpose checks, audit logs, encryption, secrets management, data minimization, rate limiting, monitoring, threat modelling and human approval for sensitive actions. This prototype is read-only and fictional.

## Learning milestones
1. Understand Python tools and LangGraph state/nodes/edges/reducers.
2. Connect to a hosted Hugging Face model (current milestone).
3. Add model-driven intent understanding and structured tool calling.
4. Connect model tool calls to approved mock banking functions through LangGraph.
5. Connect an MCP client and discover/invoke tools.
6. Add message history, error handling, tests and tracing.
7. Prepare architecture diagrams and interview explanations.

## Interview summary
"I built a fictional banking support agent to learn stateful agent workflows. LangGraph manages execution through state, nodes, edges and conditional routing. Mock functions provide read-only banking tools, while an MCP server exposes equivalent capabilities through a standard protocol. I also connected a hosted Hugging Face chat model; the next milestone is to let the model request approved tools while the application remains responsible for validation, authorization and execution."
