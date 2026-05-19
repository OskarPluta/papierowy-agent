import arxiv
import sympy
import requests

from typing import Optional

from bs4 import BeautifulSoup
from langchain_core.tools import tool 


class Tools: 

    @tool 
    def fetch_arxiv(query: str, max_results: Optional[int], sort_by: Optional[arxiv.SortCriterion], output_options: Optional[list[str]]) -> str:
        """
        Fetches results from arXiv based on the given query, maximum number of results, and sorting criterion.
        Sorting criterions can be arxiv.SortCriterion.Relevance, arxiv.SortCriterion.LastUpdatedDate, arxiv.SortCriterion.SubmittedDate, arxiv.SortCriterion.Title, arxiv.SortCriterion.Authors
        default max_results: 3, default sort_by: arxiv.SortCriterion.Relevance
        output_options is a list of strings that specifies which fields to include in the output. Possible values are "title", "summary", "authors", "published_date". If output_options is None, all fields will be included in the output.
        """
        client = arxiv.Client()

        if max_results is None:
            max_results = 3
        if sort_by is None:
            sort_by = arxiv.SortCriterion.Relevance
        search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_by)
        results = client.results(search)
        output = []
        for result in results:
            result_dict = {}
            if output_options is None or "title" in output_options:
                result_dict["title"] = result.title
            if output_options is None or "summary" in output_options:
                result_dict["summary"] = result.summary
            if output_options is None or "authors" in output_options:
                result_dict["authors"] = [author.name for author in result.authors]
            if output_options is None or "published_date" in output_options:
                result_dict["published_date"] = result.published.date()
            output.append(result_dict)
        return str(output)
    
    @tool 
    def fetch_arxiv_by_id(paper_id: str, output_options: Optional[list[str]]) -> str: # currently full content not implemented
        """Fetches a paper from arXiv based on its ID.
        The paper_id should be in the format "arXiv:xxxx.xxxxx" or "xxxx.xxxxx". For example,
        "arXiv:2101.00001" or "2101.00001".
        output_options is a list of strings that specifies which fields to include in the output. Possible values are "title", "summary", "content","authors", "published_date". If output_options is None
        all fields will be included in the output.
        """
        client = arxiv.Client()
        if paper_id.startswith("arXiv:"):
            paper_id = paper_id[6:]
        search = arxiv.Search(id_list=[paper_id], max_results=1)
        results = client.results(search)
        output = []
        for result in results:
            print(result.comment)
            print('-------')
            result_dict = {}
            if output_options is None or "title" in output_options:
                result_dict["title"] = result.title
            if output_options is None or "summary" in output_options:
                result_dict["summary"] = result.summary
            if output_options is None or "authors" in output_options:
                result_dict["authors"] = [author.name for author in result.authors]
            if output_options is None or "published_date" in output_options:
                result_dict["published_date"] = result.published.date()
            output.append(result_dict)
        return str(output)
    
    


    @tool
    def fetch_math(query: str) -> str:
        """
        Fetches the result of a mathematical expression using sympy.
        The query should be a valid mathematical expression that can be evaluated by sympy. For example, "2 + 2", "integrate(x**2, x)", "diff(sin(x), x)", etc.
        Docs are available at https://docs.sympy.org/latest/index.html
        """
        try:
            result = sympy.sympify(query)
            return str(result)
        except Exception as e:
            return f"Error: {e}" 

    @tool
    def fetch_docs(query: str) -> str:
        """
        Fetches the documentation for a given Python function or module.
        The query should be in the format "module.function" or "module". For example, "math.sqrt", "sympy.integrate", "numpy", etc.
        """
        try:
            components = query.split('.')
            if len(components) == 1:
                module = __import__(components[0])
                return module.__doc__
            else:
                module = __import__('.'.join(components[:-1]), fromlist=[components[-1]])
                func = getattr(module, components[-1])
                return func.__doc__
        except Exception as e:
            return f"Error: {e}"
        
    @tool
    def fetch_web(query: str) -> str:
        """
        Fetches the content of a web page given its URL.
        The query should be a valid URL. For example, "https://www.wikipedia.org/", "https://www.nature.com/", etc.
        """
        if not Tools.validade_url(query):
            return "Error: Invalid URL"
        
        try:
            response = requests.get(query)
            if response.status_code == 200:
                return response.text
            else:
                return f"Error: Received status code {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
        

    @staticmethod
    def clean_html_to_text(html: str) -> str:
        """
        Cleans the given HTML content and returns the plain text.
        """
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        return "\n".join(lines)


    @staticmethod
    def validade_url(url: str) -> bool:
        """
        Validates if the given string is a valid URL.
        """
        if url.startswith("http://") or url.startswith("https://"):
            return True
        return False
