import functools
import anyio.to_thread
from dataclasses import dataclass, KW_ONLY
from typing import Any, TypedDict, List, Union
from pydantic import TypeAdapter
from pydantic_ai.tools import Tool

try:
    try:
        from ddgs.ddgs import DDGS
    except ImportError:  # Fallback for older versions of ddgs
        from duckduckgo_search import DDGS
except ImportError:
    pass 

class DuckDuckGoResult(TypedDict):
    """A DuckDuckGo search result."""
    title: str
    href: str
    body: str

duckduckgo_ta = TypeAdapter(list[DuckDuckGoResult])

@dataclass
class SafeDuckDuckGoSearchTool:
    """The DuckDuckGo search tool with error handling."""

    client: 'DDGS'
    _: KW_ONLY
    max_results: int | None

    async def __call__(self, query: str) -> Union[list[DuckDuckGoResult], str]:
        search = functools.partial(self.client.text, max_results=self.max_results)
        try:
            results = await anyio.to_thread.run_sync(search, query)
            # results is typically a list of dicts or generator. 
            # pydantic_ai validate_python handles list of dicts.
            if not results:
                return "No results found."
            return duckduckgo_ta.validate_python(results)
        except Exception as e:
            return f"No results found or error occurred: {str(e)}"

def safe_duckduckgo_search_tool(duckduckgo_client: Union['DDGS', None] = None, max_results: int | None = None):
    """Creates a Safe DuckDuckGo search tool."""
    return Tool(
        SafeDuckDuckGoSearchTool(client=duckduckgo_client or DDGS(), max_results=max_results).__call__,
        name='duckduckgo_search',
        description='Searches DuckDuckGo for the given query and returns the results.',
    )
