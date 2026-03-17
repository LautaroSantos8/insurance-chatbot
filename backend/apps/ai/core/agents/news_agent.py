import requests
from dotenv import dotenv_values
from apps.ai.core.agents.base_llm_agent import BaseLLMAgent
from apps.ai.core.prompts import news_agent_initial_system_prompt, news_agent_response_execution_prompt
from common.logger import logger
env = dotenv_values()


class NewsAgent:
    """
    This class provides functionality for retrieving and processing news and learning resources.

    Attributes:

    rag_you_com (str): A rag from you.com that returns responses according to the core of the app. 
                       It provides at least 3 and at most 5 links about current news, listed by score of importance.

    normal_search (str): An API call to search news with no particular order, but with parameters focusing on the study case.

    search_resources (str): An API call to obtain learning resources related to the user's query.

    search (str): Combines the normal_search attribute with Google Gemini LLM to provide a composed answer to the user with news.

    searcher_rag (str): Combines the rag_you_com attribute with Google Gemini LLM to provide a composed answer to the user with news scored by importance.
    """

    def __init__(self, country="CL", safesearch="off"):
        self.country = country
        self.safesearch = safesearch
        self.base_url = "https://api.ydc-index.io"
        self.news_llm = BaseLLMAgent(
            model_name="gemini-1.0-pro", initial_system_prompt=news_agent_initial_system_prompt())

    def _contextualize_query(self, query: str):
        return "Buscarás noticias en Chile (dominio .cl) para la siguiente petición de un usuario: " + query,

    def rag_you_com(self, query):
        """
        Retrieves news from a specified source based on the given query.

        Args:
        query (str): The query to focus on, with results limited to Chile with a .cl domain.

        Returns:
        List: A list containing the answer and hits retrieved from the source.
        """

        url = f"{self.base_url}/rag"
        params = {
            "query": self._contextualize_query(query),
            "num_web_results": "5",
            "country": self.country,
            "safesearch": self.safesearch
        }
        headers = {"X-API-Key": env["YOU_API_KEY_RAG"]}
        response_rag = requests.get(url, headers=headers, params=params)
        answers = response_rag.json()
        total_rag = [answers.get("answer"), answers.get("hits")]
        return total_rag

    def normal_search(self, query):
        """
        Performs a normal news search based on the given query.

        Args:
        query (str): The query to search for news.

        Returns:
        List: A list of news results.
        """
        url = f"{self.base_url}/news"
        params = {
            "q": self._contextualize_query(query),
            "count": "3",
            "country": self.country
        }
        headers = {"X-API-Key": env["YOU_API_KEY_SEARCH"]}
        response = requests.get(url, headers=headers, params=params)
        answers_news = response.json()
        total_normal_search = answers_news.get("news", {}).get("results", [])
        return total_normal_search

    def search_resources(self, query):
        """
        Searches for learning resources related to the given query.

        Args:
        query (str): The query to search for learning resources.

        Returns:
        List: A list of learning resources.
        """
        url = f"{self.base_url}/search"
        params = {
            "query": query,
            "country": self.country,
            "safesearch": self.safesearch,
            "num_web_results": "3"
        }
        headers = {"X-API-Key": env["YOU_API_KEY_SEARCH"]}
        response_res = requests.get(url, headers=headers, params=params)
        answer_res = response_res.json()
        total_search_resources = answer_res.get("hits", [])
        return total_search_resources

    def search(self, prompt: str):
        """
        Combines a normal search with a response from a language model to provide a composed answer to the user.

        Args:
        prompt (str): The prompt for the search.

        Returns:
        str: The final response composed from the search results and the language model.
        """

        logger.info(f"(News Agent) Prompt: {prompt}")

        search_results = self.normal_search(query=prompt)
        logger.info(f"(News Agent) Search Results: {search_results}")

        final_response = self.news_llm.prompt(message=news_agent_response_execution_prompt(
            user_prompt=prompt,
            query_results=str(search_results)
        ))
        logger.info(f"(News Agent) Final Response: {final_response}")
        return final_response

    def rag_search(self, prompt: str):
        """
        Combines a specialized search (rag_you_com) with a response from a language model to provide a composed answer to the user.

        Args:
        prompt (str): The prompt for the search.

        Returns:
        str: The final response composed from the search results and the language model.
        """
        logger.info(f"(News Agent) Prompt: {prompt}")

        search_results = self.rag_you_com(query=prompt)
        results = []
        for i in range(len(search_results)):
            results.append([search_results[1][i]["url"], search_results[1]
                           [i]["description"], search_results[1][i]["title"]])

        logger.info(f"(News Agent) Search Results: {results}")

        final_responses = self.news_llm.prompt(message=news_agent_response_execution_prompt(
            user_prompt=prompt,
            query_results=str(results)
        ))
        logger.info(f"(News Agent) Final Response: {final_responses}")
        return final_responses

    def stream_rag_search(self, prompt: str):
        """
        Combines a specialized search (rag_you_com) with a response from a language model to provide a composed answer to the user.

        Args:
        prompt (str): The prompt for the search.

        Yields:
        str: The final response composed from the search results and the language model.
        """
        logger.info(f"(News Agent) Prompt: {prompt}")

        search_results = self.rag_you_com(query=prompt)
        results = []
        for i in range(len(search_results)):
            results.append([search_results[1][i]["url"], search_results[1]
                           [i]["description"], search_results[1][i]["title"]])

        logger.info(f"(News Agent) Search Results: {results}")

        final_response = ""
        for chunk in self.news_llm.stream_prompt(message=news_agent_response_execution_prompt(
            user_prompt=prompt,
            query_results=str(results)
        )):
            final_response += chunk
            logger.debug(f"(News Agent) Chunk: {chunk}")
            yield chunk

        logger.info(f"(News Agent) Final Response: {final_response}")
        return final_response
