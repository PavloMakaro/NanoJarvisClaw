import requests
from bs4 import BeautifulSoup
import config

def register_tools(registry):
    registry.register("visit_page", visit_page, "Visits a webpage and extracts text. Arguments: url (str).")

def visit_page(url):
    """Visits a webpage and extracts text."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()

        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text[:5000] + "\n...(truncated)" if len(text) > 5000 else text
    except Exception as e:
        return f"Error visiting page: {str(e)}"
