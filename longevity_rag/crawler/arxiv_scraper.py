import requests
import xml.etree.ElementTree as ET

def fetch_papers(query, max_results):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Failed to fetch papers:", response.status_code)
        return []
    
    #parses a string into an ElementTree Object, so you can work with a tree object, kind of like navigating folders and files
    root = ET.fromstring(response.text)
    #a unique identifier, the XML follows an Atom standard, which is a format for web feeds
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    results = []
    #all these tags belong to the atom xml namespace
    for entry in root.findall('atom:entry', namespace):
        paper = {
            "title": entry.find('atom:title', namespace).text.strip(),
            "summary": entry.find('atom:summary', namespace).text.strip(),
            "authors": [author.find('atom:name', namespace).text.strip() for author in entry.findall('atom:author', namespace)],
            "url": entry.find('atom:id', namespace).text.strip()
        }
        results.append(paper)

    return results

"""
import time

def check_peer_validity(paper, verbose=False):
   
    #Check the peer validity of a paper using Semantic Scholar's API based on the title.
    #Returns a dictionary with metadata and a validity boolean.
   

    # Sanitize title (remove line breaks, excess spaces)
    title = " ".join(paper["title"].replace("\n", " ").split())

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "title,citationCount,influentialCitationCount,venue"
    }

    headers = {
        "User-Agent": "LongevityBot/1.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            if verbose:
                print(f"Semantic Scholar API error {response.status_code} for title: {paper['title']}")
                print("Response:", response.text)
            return {"valid": False, "reason": f"API error {response.status_code}"}

        data = response.json()

        if not data.get("data"):
            if verbose:
                print(f"No match found for: {paper['title']}")
            return {"valid": False, "reason": "No match"}

        match = data["data"][0]
        citation_count = match.get("citationCount", 0)
        influential_count = match.get("influentialCitationCount", 0)
        venue = match.get("venue", "").lower()

        # Heuristic for peer validity (customized for healthcare/longevity)
        is_valid = (
            citation_count >= 30 or
            influential_count >= 5 or
            any(x in venue for x in [
                "lancet", "jama", "bmj", "nature", "nejm", "cell",
                "science", "plos", "bioinformatics", "frontiers",
                "aging", "gerontology", "longevity", "alzheimer", "neurology"
            ])
        )

        return {
            "valid": is_valid,
            "citationCount": citation_count,
            "influentialCitationCount": influential_count,
            "venue": match.get("venue", "Unknown"),
            "reason": "OK"
        }

    except Exception as e:
        if verbose:
            print(f"Exception during API call for: {paper['title']}\nError: {e}")
        return {"valid": False, "reason": "Exception occurred"}

    finally:
        time.sleep(1)  # Be respectful of API limits
"""

