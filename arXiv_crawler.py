import feedparser
import urllib.parse
import requests
import os

# Create output folder
os.makedirs("arxiv_pdfs", exist_ok=True)

def search_arxiv(query="longevity", max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    encoded_query = urllib.parse.quote(query)
    query_url = f"{base_url}?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    feed = feedparser.parse(query_url)
    
    for i, entry in enumerate(feed.entries):
        title = entry.title
        pdf_url = entry.id.replace("abs", "pdf") + ".pdf"
        filename = os.path.join("arxiv_pdfs", f"paper_{i+1}.pdf")
        
        print(f"Downloading: {title}\n → {pdf_url}")
        download_pdf(pdf_url, filename)

def download_pdf(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved: {filename}\n")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Example usage
search_arxiv("longevity biology", max_results=10)