import arxiv

client = arxiv.Client()


search = arxiv.Search(query="Kepler planetary motion", max_results=3, sort_by=arxiv.SortCriterion.Relevance)

results = client.results(search)

for result in client.results(search):
    print(result.title)
    print(result.summary)