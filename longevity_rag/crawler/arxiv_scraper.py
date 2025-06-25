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

import time


#Crossref API is best for verifying that a paper is published in a legitimate journal.


def check_peer_validity(paper, verbose=False):
    """
    Check the peer validity of a paper using Crossref API based on the title.
    Returns a dictionary with metadata and a validity boolean.
    """
    # Sanitize title
    title = " ".join(paper["title"].replace("\n", " ").split())

    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "rows": 1
    }

    headers = {
        "User-Agent": "LongevityBot/1.0 (mailto:hysi.fjona9@outlook.com)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            reason = f"API error {response.status_code}"
            if response.status_code == 429:
                reason += " - Rate limit exceeded"
            if verbose:
                print(f"Crossref API error {response.status_code} for title: {paper['title']}")
                print("Response:", response.text)
            return {"valid": False, "reason": reason}

        data = response.json()
        items = data.get("message", {}).get("items", [])

        if not items:
            reason = "No match found"
            if verbose:
                print(f"No match found for: {paper['title']}")
            return {"valid": False, "reason": reason}

        match = items[0]
        journal = match.get("container-title", ["Unknown"])[0].lower()
        doi = match.get("DOI", None)

        # Heuristic for peer-reviewed venues (you can extend this as needed)
        is_valid = doi is not None 
        """
        and any(x in journal for x in [
            "lancet", "jama", "bmj", "nature", "nejm", "cell",
            "science", "plos", "bioinformatics", "frontiers",
            "aging", "gerontology", "longevity", "alzheimer", "neurology"
        ])
        """

        reason = "Meets journal criteria" if is_valid else "Does not meet journal criteria"

        return {
            "valid": is_valid,
            "DOI": doi,
            "journal": match.get("container-title", ["Unknown"])[0],
            "reason": reason
        }

    except Exception as e:
        if verbose:
            print(f"Exception during API call for: {paper['title']}\nError: {e}")
        return {"valid": False, "reason": f"Exception: {e}"}

    finally:
        time.sleep(2)  # Respect API rate limits (adjust delay as needed)
