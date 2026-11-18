# Banking AI Support Agent

An educational project for learning Python, LangGraph, LangChain, MCP and LLM tool calling through a fictional banking support use case.

> Safety: this project uses fictional in-memory data only. It is not connected to a bank or payment network. Never commit real customer data, credentials, tokens or account details.

## What you will learn
- Difference between an LLM, an agent and a workflow.
- Tool calling: the model requests a tool; the application validates and executes it.
- MCP: standardized discovery and invocation of tools through a client/server protocol.
- LangGraph: StateGraph, state, nodes, edges, conditional routing and reducers.
- Reliability concepts to add later: validation, retries, checkpointing and human approval.

## Architecture
Customer query -> LangGraph workflow -> intent classification -> conditional route.
Balance, transaction and card-status requests call read-only mock functions. General questions follow a separate response path. An MCP server exposes equivalent mock functions over stdio. In a later milestone, an MCP client and an LLM with tool-calling support will connect the pieces.

This first milestone deliberately uses deterministic routing. It does not claim that keyword matching is LLM reasoning. We first isolate graph mechanics, then add model tool calling and MCP-client integration.

## Structure
- app/state.py: shared graph state and reducer example
- app/banking_tools.py: fictional read-only banking functions
- app/graph.py: LangGraph nodes, edges and conditional routing
- app/main.py: runnable examples
- mcp_server/server.py: MCP server exposing tools
- tests/test_graph.py: basic tests
- docs/concepts.md: interview-oriented explanations

## Setup
Python 3.11+ recommended.

Windows PowerShell:
    py -3.11 -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt

macOS/Linux:
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Run the graph from the repository root:
    python -m app.main

Run tests:
    python -m pytest

Run the MCP server:
    python -m mcp_server.server

The MCP server uses stdio. It is intended to be launched by an MCP host/client, not used as a normal interactive terminal command.

## Key concepts
| Concept | Meaning | Project example |
|---|---|---|
| State | Shared data passed between nodes | query, intent, result |
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
2. Run and inspect the MCP server.
3. Connect an MCP client and discover/invoke tools.
4. Add an LLM that selects approved tools using structured tool calling.
5. Add message history, error handling, tests and tracing.
6. Prepare architecture diagrams and interview explanations.

## Interview summary
"I built a fictional banking support agent to learn stateful agent workflows. LangGraph manages execution through state, nodes, edges and conditional routing. Mock functions provide read-only banking tools, while an MCP server exposes equivalent capabilities through a standard protocol. The next integration layer lets an LLM request tools, while the host application remains responsible for validation, authorization and execution."
