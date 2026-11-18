"""MCP server publishing the fictional banking tools over stdio.

Launch using: python -m mcp_server.server
An MCP host/client should launch this process. stdout is reserved for the
protocol when using stdio; avoid ordinary print statements here.
"""

from mcp.server.fastmcp import FastMCP

from app.banking_tools import get_account_balance, get_card_status, get_recent_transactions

mcp = FastMCP("demo-banking-tools")


@mcp.tool()
def account_balance(account_id: str = "DEMO-001") -> str:
    """Get the balance of a fictional demo account."""
    return get_account_balance(account_id)


@mcp.tool()
def recent_transactions(account_id: str = "DEMO-001", limit: int = 3) -> list[dict]:
    """Get recent transactions for a fictional demo account."""
    return get_recent_transactions(account_id, limit)


@mcp.tool()
def debit_card_status(account_id: str = "DEMO-001") -> str:
    """Get the status of a fictional demo debit card."""
    return get_card_status(account_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
