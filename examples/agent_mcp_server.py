from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def get_name():
    """
    Get the name of a person.
    Returns:
        str: The name of the person.
    """
    return f"Alice"

@mcp.tool
def set_age(age:int):
    """
    Set the age of a person.
    Args:
        age (int): The age of the person.
    Returns:
        str: A success message.
    """
    return f"success"

@mcp.tool
def set_name(name:str):
    """
    Set the name of a person.
    Args:
        name (str): The name of the person.
    Returns:
        str: A success message.
    """
    return f"success"

@mcp.tool
def get_age():
    """
    Get the age of a person.
    Returns:
        int: The age of the person.
    """
    return 100

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)
