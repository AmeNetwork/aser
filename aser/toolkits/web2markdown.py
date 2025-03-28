import requests
from bs4 import BeautifulSoup
import html2text
import re
def clear_up(markdown_content):

    cleaned_content = re.sub(r'^\s*\*.*$', '', markdown_content, flags=re.MULTILINE)
    

    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
    

    cleaned_content = cleaned_content.strip()
    
    return cleaned_content

def web_to_markdown(url):

    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    main_content = soup.find("article")
    if main_content is None:
        main_content = soup.body

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.ignore_tables = True
    h.ignore_anchors = True
    markdown_content = h.handle(str(main_content))
    markdown_content_handled=clear_up(markdown_content)

    return markdown_content_handled


web2markdown = [
    {
        "name": "web_to_markdown",
        "description": "get markdown content by web url",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "web url",
                }
            },
            "required": ["url"],
        },
        "function": web_to_markdown,
        "extra_prompt": None,
        "example": None,
    }
]


