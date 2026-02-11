from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("users-mcp-server")

@mcp.tool()
def get_user_data(user_id: int) -> dict:
    """ Use this tool to get user data by their ID """
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    return response.json()

mcp.run(transport="stdio")
