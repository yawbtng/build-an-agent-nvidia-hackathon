import os
import asyncio
from typing import List, Union, Dict, Any, Optional, cast
from tavily import TavilyClient, AsyncTavilyClient
from langchain_nvidia_ai_endpoints import ChatNVIDIA


def _set_env(var: str) -> None:
    """Set environment variable if not already set."""
    if not os.environ.get(var):
        import getpass
        os.environ[var] = getpass.getpass(f"{var}: ")


def setup_environment() -> None:
    """Setup environment variables and API keys."""
    # NVIDIA API Key setup
    if not os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
        import getpass
        nvapi_key = getpass.getpass("Enter your NVIDIA API key: ")
        assert nvapi_key.startswith("nvapi-"), f"{nvapi_key[:5]}... is not a valid key"
        os.environ["NVIDIA_API_KEY"] = nvapi_key

    # LangChain setup
    _set_env("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "report-mAIstro"

    # Tavily setup
    _set_env("TAVILY_API_KEY")


# Initialize clients and LLM
tavily_client: TavilyClient = TavilyClient()
tavily_async_client: AsyncTavilyClient = AsyncTavilyClient()
llm: ChatNVIDIA = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)


def deduplicate_and_format_sources(
    search_response: Union[Dict[str, Any], List[Dict[str, Any]]],
    max_tokens_per_source: int,
    include_raw_content: bool = True
) -> str:
    """
    Deduplicate and format search results into a readable string.

    Args:
        search_response: Search results from Tavily API
        max_tokens_per_source: Maximum tokens to include per source
        include_raw_content: Whether to include raw content from sources

    Returns:
        Formatted string of sources
    """
    # Normalize search_response to a list of sources
    sources_list: List[Dict[str, Any]] = []

    if isinstance(search_response, dict):
        sources_list = search_response.get('results', [])
    elif isinstance(search_response, list):
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                sources_list.extend(response['results'])
            elif isinstance(response, list):
                response = cast(List[Dict[str, Any]], response)
                sources_list.extend(response)
            else:
                sources_list.append(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")

        # Deduplicate by URL
    unique_sources: Dict[str, Dict[str, Any]] = {}
    for source in sources_list:
        if isinstance(source, dict) and 'url' in source:
            source_url: str = source['url']
            if source_url not in unique_sources:
                unique_sources[source_url] = source

    # Format sources
    formatted_text: str = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
        title: str = source.get('title', 'Unknown Title')
        url: str = source.get('url', 'Unknown URL')
        content: str = source.get('content', 'No content available')

        formatted_text += f"Source {title}:\n===\n"
        formatted_text += f"URL: {url}\n===\n"
        formatted_text += f"Most relevant content from source: {content}\n===\n"

        if include_raw_content:
            char_limit: int = max_tokens_per_source * 4  # Rough estimate: 4 chars per token
            raw_content: str = source.get('raw_content', '')
            if raw_content is None:
                raw_content = ''
                print(f"Warning: No raw_content found for source {url}")

            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"

    return formatted_text.strip()


def format_sections(sections: List[Any]) -> str:
    """
    Format sections into a readable string.

    Args:
        sections: List of Section objects

    Returns:
        Formatted string of sections
    """
    formatted_str: str = ""
    for idx, section in enumerate(sections, 1):
        formatted_str += f"""
{'='*60}
Section {idx}: {section.name}
{'='*60}
Description:
{section.description}
Requires Research:
{section.research}

Content:
{section.content if section.content else '[Not yet written]'}

"""
    return formatted_str


def tavily_search(query: str) -> Dict[str, Any]:
    """
    Perform a single synchronous search using Tavily.

    Args:
        query: Search query string

    Returns:
        Search results from Tavily
    """
    try:
        return tavily_client.search(query, max_results=5, include_raw_content=True)
    except Exception as e:
        print(f"Error in tavily_search for query '{query}': {e}")
        return {"results": []}


async def tavily_search_async(
    search_queries: List[str],
    tavily_topic: str,
    tavily_days: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Perform multiple asynchronous searches using Tavily.

    Args:
        search_queries: List of search query strings
        tavily_topic: Topic type ("news" or "general")
        tavily_days: Number of days for news search (only for news topic)

    Returns:
        List of search results from Tavily
    """
    search_tasks: List[Any] = []

    for query in search_queries:
        try:
            if tavily_topic == "news":
                # Only pass days parameter if tavily_days is not None
                if tavily_days is not None:
                    task = tavily_async_client.search(
                        query,
                        max_results=5,
                        include_raw_content=True,
                        topic="news",
                        days=tavily_days
                    )
                else:
                    task = tavily_async_client.search(
                        query,
                        max_results=5,
                        include_raw_content=True,
                        topic="news"
                    )
            else:
                task = tavily_async_client.search(
                    query,
                    max_results=5,
                    include_raw_content=True,
                    topic="general"
                )
            search_tasks.append(task)
        except Exception as e:
            print(f"Error creating search task for query '{query}': {e}")
            # Create a dummy task that returns empty results
            async def empty_result() -> Dict[str, Any]:
                return {"results": []}
            search_tasks.append(empty_result())

    try:
        results: List[Any] = await asyncio.gather(*search_tasks, return_exceptions=True)

        # Handle any exceptions in the results
        processed_results: List[Dict[str, Any]] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error in search task {i}: {result}")
                processed_results.append({"results": []})
            else:
                processed_results.append(result)

        return processed_results
    except Exception as e:
        print(f"Error in tavily_search_async: {e}")
        return [{"results": []} for _ in search_queries]