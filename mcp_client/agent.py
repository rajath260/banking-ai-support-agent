"""Run the Hugging Face agent with tools discovered from the local MCP server."""

import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from app.llm import get_client
from app.mcp_agent_graph import build_mcp_agent_graph
from mcp_client.client import discover_tools, server_parameters


async def run_mcp_agent(question: str) -> dict:
    """Keep the MCP session alive while the LangGraph agent uses its tools."""
    if not question or not question.strip():
        raise ValueError("question must not be empty")

    model_client = get_client()
    async with stdio_client(server_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await discover_tools(session)
            graph = build_mcp_agent_graph(
                session=session,
                discovered_tools=tools,
                client=model_client,
            )
            return await graph.ainvoke(
                {"user_query": question.strip(), "trace": []}
            )


async def main() -> None:
    print("Banking AI Support Agent (MCP-connected demo data)")
    print("Available tools are discovered from the MCP server at startup.")
    question = input("\nYou: ").strip()
    if not question:
        print("Please enter a question.")
        return

    result = await run_mcp_agent(question)
    print("\nAssistant:", result.get("final_response", "No response generated."))
    print("\nExecution trace:")
    for item in result.get("trace", []):
        print(" -", item)


if __name__ == "__main__":
    asyncio.run(main())
