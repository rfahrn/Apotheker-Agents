# tools/tavily_fallback.py
import os
from tavily import TavilyClient
import streamlit as st
api_key_tavily = st.secrets["tavily"]["TAVILY_API_KEY"]
client = TavilyClient(api_key=api_key_tavily)


def tavily_web_search(query, num_results=3):
    try:
        print("🌐 Führe allgemeine Websuche...")
        
        results = client.search(
            query=query,
            search_depth="advanced",
            include_answer="advanced",
            max_results=num_results,
            include_images=True,
            include_image_descriptions=True,
            include_raw_content=True,
        )
        
        urls = [item.get("url") for item in results.get("results", [])]
        
        if not urls:
            return "❗ Keine relevanten Links gefunden."
        
        response = "**🔗 Gefundene Links:**\n"
        for idx, url in enumerate(urls, start=1):
            response += f"{idx}. {url}\n"
        
        return response
    
    except Exception as e:
        print(f"❗ Fehler bei Tavily Websuche: {e}")
        return "❗ Fehler bei Websuche."

