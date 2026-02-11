from mcp.server.fastmcp import FastMCP
import requests
mcp = FastMCP('name-origin')

@mcp.tool()
def predict_origin(name: str) -> dict:
    """ 
    Use this tool to get the origin of a name.
    
    Args: 
        name (str): The name to predict the origin for.
        
    returns:
        dict: A dictionary containing the predicted origin.
    """
    response = requests.get(f"http://api.nationalize.io/?name={name}")
    return response.json()
    
mcp.run(transport='stdio')