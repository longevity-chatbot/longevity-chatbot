import feedparser
import urllib.parse
import requests
from langchain.docstore.document import Document
import fitz  # pip install pymupdf

def extract_text_from_pdf(pdf_bytes):
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)


def search_arxiv(query="longevity biology", max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    encoded_query = urllib.parse.quote(query)
    query_url = f"{base_url}?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    feed = feedparser.parse(query_url)
    
    docs = []
    
    for entry in feed.entries:
        pdf_url = entry.id.replace("abs", "pdf") + ".pdf"
        try: 
            pdf_bytes = requests.get(pdf_url).content
             #uses the whole document, not just summary
            full_text = extract_text_from_pdf(pdf_bytes)
        except Exception as e:
            print(f"Failed to process {pdf_url}: {e}")
            continue
        
        doc = Document (page_content=full_text,
                        metadata = {
                            "title": entry.title,
                            "summary": entry.summary,
                            "pdf_url": pdf_url,
                            "published": entry.published
                        })

        docs.append(doc)
        return docs
    

