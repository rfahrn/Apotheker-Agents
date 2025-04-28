from dotenv import load_dotenv
import os
load_dotenv()
from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient

api_key_tavily = st.secrets["tavily"]["TAVILY_API_KEY"]
client = TavilyClient(api_key=api_key_tavily)

def get_compendium_info(medication: str) -> str:
    query = f"site:compendium.ch {medication}"
    results = client.search(query=query, search_depth="advanced", include_answer=True)

    answer = results.get("answer")
    urls = [r["url"] for r in results.get("results", [])]

    if not answer or not urls:
        return None  # ❗ No valid answer or no links -> treat as no result
    
    response = f"**Info für '{medication}':**\n\n{answer}\n\n🔗 Links:\n"
    response += "\n".join(f"- {url}" for url in urls[:3])
    return response



