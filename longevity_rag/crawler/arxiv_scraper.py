
import arxiv

def fetch_papers(query="longevity", max_results=10):
    search = arxiv.Search(query=query, max_results=max_results)
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "authors": [a.name for a in result.authors],
            "url": result.entry_id
        })
    print(papers)
    return papers
