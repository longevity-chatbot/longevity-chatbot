import requests

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
    
    papers = []
    
    for entry in results:
        papers.append({
            "title": entry.get("title", ""),
            "summary": entry.get("abstractText", ""),
            "source":"EuropePMC",
            "published": entry.get("pubYear", ""),
            "doi": entry.get("doi", ""),
            "fullTextUrl": entry.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", "")
        })
        
    return papers