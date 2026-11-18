"""Offline tests for the MCP-connected LangGraph agent."""

from types import SimpleNamespace

import pytest

from app.mcp_agent_graph import build_mcp_agent_graph, mcp_tools_to_llm_tools


DISCOVERED_TOOLS = [
    {
        "name": "account_balance",
        "description": "Get the fictional demo account balance.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "recent_transactions",
        "description": "Get recent transactions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "minimum": 1, "maximum": 5}
            },
            "required": [],
        },
    },
]


def sdk_message(content="", tool_calls=None):
    return SimpleNamespace(content=content, tool_calls=tool_calls or [])


def sdk_response(message):
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeCompletions:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.responses)


def fake_model_client(responses):
    completions = FakeCompletions(responses)
    client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
    return client, completions


class FakeMCPSession:
    def __init__(self):
        self.calls = []

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return SimpleNamespace(
            content=[
                SimpleNamespace(type="text", text="Account balance: INR 45,000.00")
            ],
            isError=False,
        )


def test_mcp_schemas_are_converted_to_llm_function_tools():
    tools = mcp_tools_to_llm_tools(DISCOVERED_TOOLS)

    assert [item["function"]["name"] for item in tools] == [
        "account_balance",
        "recent_transactions",
    ]
    assert "limit" in tools[1]["function"]["parameters"]["properties"]


@pytest.mark.anyio
async def test_agent_uses_discovered_mcp_tool_and_returns_model_answer():
    requested_tool = SimpleNamespace(
        id="call_balance_1",
        function=SimpleNamespace(
            name="account_balance",
            arguments="{}",
        ),
    )
    client, completions = fake_model_client(
        [
            sdk_response(sdk_message(tool_calls=[requested_tool])),
            sdk_response(sdk_message("Your demo account balance is INR 45,000.00.")),
        ]
    )
    session = FakeMCPSession()
    graph = build_mcp_agent_graph(session, DISCOVERED_TOOLS, client=client)

    result = await graph.ainvoke(
        {"user_query": "What is my account balance?", "trace": []}
    )

    assert "INR 45,000.00" in result["final_response"]
    assert session.calls == [("account_balance", {})]
    assert len(completions.calls) == 2
    assert completions.calls[0]["tools"][0]["function"]["name"] == "account_balance"
    assert any("invoked 1 requested tool" in item for item in result["trace"])


@pytest.mark.anyio
async def test_agent_answers_general_question_without_mcp_call():
    client, completions = fake_model_client(
        [sdk_response(sdk_message("A savings account is used to save money."))]
    )
    session = FakeMCPSession()
    graph = build_mcp_agent_graph(session, DISCOVERED_TOOLS, client=client)

    result = await graph.ainvoke(
        {"user_query": "What is a savings account?", "trace": []}
    )

    assert result["final_response"] == "A savings account is used to save money."
    assert session.calls == []
    assert len(completions.calls) == 1


@pytest.mark.anyio
async def test_agent_rejects_tool_name_not_discovered_from_mcp_server():
    unknown_tool = SimpleNamespace(
        id="call_unknown_1",
        function=SimpleNamespace(name="delete_account", arguments="{}"),
    )
    client, _ = fake_model_client(
        [
            sdk_response(sdk_message(tool_calls=[unknown_tool])),
            sdk_response(sdk_message("I could not perform that operation.")),
        ]
    )
    session = FakeMCPSession()
    graph = build_mcp_agent_graph(session, DISCOVERED_TOOLS, client=client)

    result = await graph.ainvoke(
        {"user_query": "Delete my account", "trace": []}
    )

    assert session.calls == []
    assert "not discovered" in result["tool_results"][0]["content"]
