import requests
from bs4 import BeautifulSoup
import config
from duckduckgo_search import DDGS

def register_tools(registry):
    registry.register("google_search", google_search, "Searches the web using LangSearch (Google wrapper). Arguments: query (str).")
    registry.register("duckduckgo_search", duckduckgo_search, "Searches the web using DuckDuckGo. Arguments: query (str).")
    registry.register("visit_page", visit_page, "Visits a webpage and extracts text. Arguments: url (str).")

def google_search(query):
    """Searches the web using LangSearch API."""
    url = "https://api.langsearch.com/v1/web-search"
    headers = {
        "Authorization": f"Bearer {config.LANGSEARCH_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "count": 5
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json().get("webPages", {}).get("value", [])

        formatted_results = []
        for item in results:
            formatted_results.append(f"Title: {item.get('name')}\nURL: {item.get('url')}\nSnippet: {item.get('snippet')}\n")

        return "\n".join(formatted_results) if formatted_results else "No results found."
    except Exception as e:
        return f"Error searching web: {str(e)}"

def duckduckgo_search(query):
    """Searches the web using DuckDuckGo."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."

        formatted_results = []
        for item in results:
            formatted_results.append(f"Title: {item.get('title')}\nURL: {item.get('href')}\nSnippet: {item.get('body')}\n")

        return "\n".join(formatted_results)
    except Exception as e:
        return f"Error searching DuckDuckGo: {str(e)}"

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
