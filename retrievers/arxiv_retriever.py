import feedparser
import urllib.parse

def search_arxiv(query="longevity biology", max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    encoded_query = urllib.parse.quote(query)
    query_url = f"{base_url}?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    feed = feedparser.parse(query_url)
    
    papers = []
    
    for entry in feed.entries:
        pdf_url = entry.id.replace("abs", "pdf") + ".pdf"
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "pdf_url": pdf_url,
            "published": entry.published
        })
        
    return papers