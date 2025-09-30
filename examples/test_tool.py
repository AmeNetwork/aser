import requests



def custom_tool_1759223998(url: str) -> str:
    """
    Fetch and return the content of a GitHub README file from a given URL.

    Parameters:
        url (str): A URL pointing to a GitHub README.md file, expected in the format
                   'https://github.com/{user}/{repo}/blob/{branch}/README.md'.

    Returns:
        str: The raw content of the README.md file.

    Raises:
        ValueError: If the URL format is invalid or does not point to a GitHub README.md file.
        ConnectionError: If there is a network-related error.
        requests.HTTPError: If the HTTP request to fetch the file fails (non-200 response).
    """
    try:
        # Validate and convert GitHub blob URL to raw URL
        if not url.startswith("https://github.com/") or "/blob/" not in url or not url.endswith("README.md"):
            raise ValueError("Invalid GitHub README URL format.")

        raw_url = url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")

        resp = requests.get(raw_url, timeout=10)
        resp.raise_for_status()
        return resp.text

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error occurred: {e}") from e


readme_content = custom_tool_1759223998("https://github.com/AmeNetwork/aser/blob/main/README.md")
print(readme_content)
