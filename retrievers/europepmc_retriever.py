import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document

def extract_full_text_from_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Heuristically extract text from <p> tags
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return "\n".join(paragraphs).strip()
    except Exception as e:
        print(f"⚠️ Failed to extract full text from {url}: {e}")
        return None


def search_europe_pmc(query="longevity biology", limit = 10):
    base_url="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "pageSize": limit,
        "resultType": "core"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    results = response.json()["resultList"]["result"]
    
    documents = []
    
    for entry in results:
            title= entry.get("title", "")
            abstract= entry.get("abstractText", "")
            year= entry.get("pubYear", "")
            doi= entry.get("doi", "")
            fulltext_urls = entry.get("fullTextUrlList", {}).get("fullTextUrl", [])
            
            full_text = None
            for url_entry in fulltext_urls:
                if url_entry.get("documentStyle" == "html"):
                    full_text = extract_full_text_from_html(url_entry["url"])
                    if full_text:
                        break
            
            # fallback to abstract if no full text available
            page_content = full_text if full_text else abstract
            if not page_content:
                continue
            
            doc = Document(
            page_content=page_content,
            metadata={
                "title": title,
                "source": "EuropePMC",
                "published": year,
                "doi": doi
                }
            )
            documents.append(doc)

    return documents