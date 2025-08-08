import requests
import xml.etree.ElementTree as ET
import time

def fetch_pubmed_papers(query, max_results=10):
    """Fetch papers from PubMed using E-utilities API"""
    
    # Step 1: Search for paper IDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml",
        "sort": "relevance"
    }
    
    search_response = requests.get(search_url, params=search_params)
    if search_response.status_code != 200:
        print(f"PubMed search failed: {search_response.status_code}")
        return []
    
    # Parse search results to get PMIDs
    search_root = ET.fromstring(search_response.text)
    pmids = [id_elem.text for id_elem in search_root.findall(".//Id")]
    
    if not pmids:
        print("No PubMed papers found")
        return []
    
    # Step 2: Fetch paper details
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    
    time.sleep(0.5)  # Be nice to NCBI servers
    fetch_response = requests.get(fetch_url, params=fetch_params)
    if fetch_response.status_code != 200:
        print(f"PubMed fetch failed: {fetch_response.status_code}")
        return []
    
    # Parse paper details
    fetch_root = ET.fromstring(fetch_response.text)
    papers = []
    
    for article in fetch_root.findall(".//PubmedArticle"):
        try:
            # Extract title
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title"
            
            # Extract abstract
            abstract_elem = article.find(".//AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
            
            # Extract authors
            authors = []
            for author in article.findall(".//Author"):
                lastname = author.find("LastName")
                forename = author.find("ForeName")
                if lastname is not None and forename is not None:
                    authors.append(f"{forename.text} {lastname.text}")
            
            # Extract PMID for URL
            pmid_elem = article.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else ""
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
            
            # Extract publication year
            pub_year = ""
            pub_date = article.find(".//PubDate")
            if pub_date is not None:
                year_elem = pub_date.find("Year")
                if year_elem is not None:
                    pub_year = year_elem.text
            
            paper = {
                "title": title.strip(),
                "summary": abstract.strip(),
                "authors": authors,
                "url": url,
                "source": "PubMed",
                "year": pub_year
            }
            papers.append(paper)
            
        except Exception as e:
            print(f"Error parsing PubMed article: {e}")
            continue
    
    return papers