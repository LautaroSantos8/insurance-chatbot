from config.paths import DJANGO_SQLITE_DB_PATH
from apps.ai.core.agents.base_llm_agent import BaseLLMAgent
from apps.ai.core.chroma import ChromaManager
from apps.ai.core.prompts import general_agent_system_prompt, db_agent_response_system_prompt, db_agent_response_execution_prompt
from apps.ai.core.agents.news_agent import NewsAgent
from langchain.prompts import ChatPromptTemplate
from django.apps import apps
from common.logger import logger
from apps.users.models import User
import sqlite3
import sqlparse


class GeneralAgent(BaseLLMAgent):
    """
    GeneralAgent class for implementing a general-purpose conversational agent.

    This agent interacts with users through natural language input and provides responses based on various sources of information,
    including database queries and external APIs.
    """

    def __init__(
        self,
        db_path: str = DJANGO_SQLITE_DB_PATH,
        user_id: str = None,
        reset_history: bool = False
    ):
        super().__init__(model_name='gemini-1.5-pro',
                         initial_system_prompt=general_agent_system_prompt())

        self.db_path = db_path
        self.db_response_llm = BaseLLMAgent(
            initial_system_prompt=db_agent_response_system_prompt(), model_name='gemini-1.5-pro')

        self.chroma_manager: ChromaManager = apps.get_app_config(
            'config').chroma_manager_instance
        self.filter_prohibited = True
        self.top_k = 10

        self.user = None

        if user_id is not None:
            self.user = User.objects.get(id=user_id)
            if reset_history:
                self.user.chat_history = []
                self.user.save()
                logger.debug(
                    f"(General Agent) Chat history reset for user {self.user.id}")
            else:
                self.load_chat_history()

            logger.debug(f"(General Agent) Initialized for user {user_id}")

    def _is_read_only_query(self, query: str):
        """
        Checks if the provided SQL query is read-only.

        Args:
        query (str): The SQL query to check.

        Returns:
        bool: True if the query is read-only, False otherwise.
        """
        parsed = sqlparse.parse(query)

        for token in parsed[0].tokens:
            if isinstance(token, sqlparse.sql.Token) and token.value.upper() in ('INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE'):
                return False

        return True

    def _execute_sql_query(self, query: str):
        if not self._is_read_only_query(query):
            return None

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def _db_agent_response(self, prompt: str, query: str, query_results: str):
        """
        Generates a response based on the provided prompt, SQL query, and query results.

        Args:
        prompt (str): The prompt received by the agent.
        query (str): The SQL query executed by the agent.
        query_results (str): The results of the SQL query execution.

        Returns:
        str: The generated response.
        """
        response = self.db_response_llm.prompt(
            db_agent_response_execution_prompt(prompt, query, query_results))
        return response

    def prompt(self, message: str):
        message_history = [
            ("system", self.initial_system_prompt),
            *self.transform_history(self.history, output_type="langchain"),
            ("human", "{input}")
        ]
        logger.debug(
            f"(General Agent) {len(message_history)} messages in history.")

        self.qa = ChatPromptTemplate.from_messages(message_history)
        logger.debug(f"(General Agent) QA Prompt: {self.qa}")
        self.chain = self.qa | self.llm | self.str_output_parser

        logger.info(f"(General Agent) Received: {message}")
        response = self.chain.invoke({"input": message})

        final_response = self._process_agent_output(
            user_prompt=message,
            agent_output=response
        )

        self.history.append({
            "role": "human",
            "message": message
        })
        self.history.append({
            "role": "ai",
            "message": final_response
        })

        response = self.clean_response(final_response)

        if self.user is not None:
            self.save_chat_history()

        logger.info(f"(General Agent) Response: {response}")
        return final_response

    def save_chat_history(self):
        """
        Saves the chat history for the current user.
        """
        self.user.chat_history = self.history
        self.user.save()
        logger.debug(
            f"Chat history saved for user {self.user.id} ({len(self.user.chat_history)} messages)")

    def load_chat_history(self):
        """
        Loads the chat history for the current user.
        """
        user = self.user

        if len(user.chat_history) == 0 or user.chat_history is None:
            logger.info(f"No chat history for user {user.id} (0 messages)")
        else:
            print(user.chat_history)
            self.history = user.chat_history
            logger.info(
                f"Chat history loaded for user {user.id} ({len(user.chat_history)} messages)")

    def _process_agent_output(self, agent_output: str, user_prompt: str):
        """
        Processes the output generated by the agent.

        Args:
        agent_output (str): The output generated by the agent.
        user_prompt (str): The prompt received from the user.

        Returns:
        str: The final response generated by the agent.
        """
        if agent_output.startswith("```sql"):
            agent_output = agent_output.replace("```sql", "SQL|")

        action = agent_output.split("|")[0]
        action = action.strip()
        logger.info(f"ACTION: {action}")

        if action.startswith("SQL"):
            sql_query = agent_output.split("|")[1] \
                .replace("`sql", "").replace("`", "").strip()
            logger.info(f"(General Agent) SQL Query: {sql_query}")

            results = self._execute_sql_query(sql_query)

        elif action.startswith("TITLE_HYBRID_SEARCH"):
            hybrid_query = agent_output.replace("TITLE_HYBRID_SEARCH|", "")
            hybrid_query = hybrid_query.replace("`", "")
            hybrid_query = hybrid_query.strip()
            logger.info(f"(General Agent) Hybrid Query: {hybrid_query}")

            results = self.hybrid_title_search(hybrid_query)

        elif action.startswith("NEWS_SEARCH"):
            news_agent = NewsAgent()
            news_query = agent_output.replace("NEWS_SEARCH|", "")
            logger.info(f"(General Agent) News Query: {news_query}")

            final_news_response = news_agent.rag_search(news_query)
            return final_news_response

        elif action.startswith("DIRECT_RESPONSE"):
            direct_response = agent_output.replace("DIRECT_RESPONSE|", "")
            logger.debug(f"(General Agent) Direct response: {direct_response}")
            return direct_response

        else:
            if agent_output is not None:
                logger.error(
                    f"(General Agent) Insecure prompt. Response: {agent_output}")
                return agent_output

            else:
                results = "No results found."

        if isinstance(results, str) and results.startswith("FINAL_RESPONSE|"):
            final_response = results.replace("FINAL_RESPONSE|", "")

        else:
            logger.info(f"(General Agent) Results: {results}")
            final_response = self._db_agent_response(
                user_prompt, agent_output, results)

        logger.info(f"(General Agent) Final Response: {final_response}")
        self.db_response_llm.clear_history()

        return final_response

    def _process_agent_output_stream(self, agent_output: str, user_prompt: str):
        """
        Processes the output generated by the agent in a streaming fashion.

        Args:
        agent_output (str): The output generated by the agent.
        user_prompt (str): The prompt received from the user.

        Yields:
            str: Final response parts generated by the agent.
        """
        if agent_output.startswith("```sql"):
            agent_output = agent_output.replace("```sql", "SQL|")

        action = agent_output.split("|")[0]
        action = action.strip()
        logger.info(f"ACTION: {action}")

        if action.startswith("SQL"):
            sql_query = agent_output.split("|")[1] \
                .replace("`sql", "").replace("`", "").strip()
            logger.info(f"(General Agent) SQL Query: {sql_query}")

            results = self._execute_sql_query(sql_query)

        elif action.startswith("TITLE_HYBRID_SEARCH"):
            hybrid_query = agent_output.replace("TITLE_HYBRID_SEARCH|", "")
            hybrid_query = hybrid_query.replace("`", "")
            hybrid_query = hybrid_query.strip()
            logger.info(f"(General Agent) Hybrid Query: {hybrid_query}")

            results = self.hybrid_title_search(hybrid_query)

        elif action.startswith("NEWS_SEARCH"):
            news_agent = NewsAgent()
            news_query = agent_output.replace("NEWS_SEARCH|", "")
            logger.info(f"(General Agent) News Query: {news_query}")

            final_news_response = ""
            for chunk in news_agent.stream_rag_search(news_query):
                logger.debug(f"News response chunk: {chunk}")
                final_news_response += chunk
                yield chunk

            return final_news_response

        elif action.startswith("DIRECT_RESPONSE"):
            direct_response = agent_output.replace("DIRECT_RESPONSE|", "")
            # yield direct_response
            logger.debug(f"(General Agent) Direct response: {direct_response}")
            return direct_response

        else:
            if agent_output is not None:
                logger.error(
                    f"(General Agent) No action specified in prompt. Response: {agent_output}")
                return agent_output

            else:
                results = "No results found."

        if isinstance(results, str) and results.startswith("FINAL_RESPONSE|"):
            final_response = results.replace("FINAL_RESPONSE|", "")
            yield final_response
            self.db_response_llm.clear_history()
            logger.info(f"(General Agent) Final Response: {final_response}")
            return final_response

        else:
            logger.info(f"(General Agent) Results: {results}")
            final_response = ''
            for chunk in self.db_response_llm.stream_prompt(
                db_agent_response_execution_prompt(
                    user_prompt, agent_output, results)
            ):
                logger.debug(f"(General Agent) response chunk: {chunk}")
                final_response += chunk
                yield chunk

        logger.info(f"(General Agent) Final Response: {final_response}")
        self.db_response_llm.clear_history()

        return final_response

    def _vector_search(self, query: str):
        """
        Performs vector search based on the provided query.

        Args:
        query (str): The query for vector search.

        Returns:
        Any: The results of the vector search.
        """
        top_k = self.top_k
        filters = {"is_prohibited": False} if self.filter_prohibited else {}
        results = self.chroma_manager.similarity_search(
            collection_name='documents',
            query=query,
            top_k=top_k,
            metadata_filters=filters
        )
        return results

    def hybrid_title_search(self, title: str, result_type="LLM"):
        """
        Performs a hybrid search for policies with the provided title.

        Args:
        title (str): The title of the policies to search for.

        Returns:
        Any: The results of the hybrid search.
        """
        def clean_title(title: str):
            return title.replace("`", "").replace('"', "").replace("?", "").strip().upper()

        def execute_query(query):
            logger.info(f"(General Agent) Query: {query}")
            return self._execute_sql_query(query)

        def format_results(results):
            return ''.join([f"- {code}: {title}\n" for code, title in results])

        title = clean_title(title)
        logger.debug(f"Checking for multiple policies with title: {title}")

        results_count_query = f"SELECT COUNT(*) FROM docs_policy WHERE title = '{title}'"
        results_count = execute_query(results_count_query)[0][0]
        logger.info(f"Exact title matches: {results_count}")

        if results_count == 0:
            similar_titles_count_query = f"SELECT COUNT(*) FROM docs_policy WHERE title LIKE '%{title}%' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
            similar_titles_count = execute_query(
                similar_titles_count_query)[0][0]
            logger.info(f"Similar title matches: {similar_titles_count}")

            if similar_titles_count == 0:
                vector_search_results = self._vector_search(title)
                logger.debug(f"Vector search results: {vector_search_results}")
                print(vector_search_results)
                distances, metadatas, ids = vector_search_results["distances"][
                    0], vector_search_results["metadatas"][0], vector_search_results["ids"][0]

                result_list = [{"code": pol_id, "title": metadata["title"], "distance": distance}
                               for distance, metadata, pol_id in zip(distances, metadatas, ids)]
                result_list = sorted(result_list, key=lambda x: x["distance"])

                formatable_results = [(pol_id, metadata["title"])
                                      for metadata, pol_id in zip(metadatas, ids)]

                print(formatable_results)

                if result_type == "LLM":
                    return f"FINAL_RESPONSE|No encontré ninguna póliza con el título exacto '{title}'. Sin embargo, aquí tienes las {self.top_k} pólizas más similares que encontré:\n{format_results(formatable_results)}"
                return result_list

            elif similar_titles_count == 1:
                similar_policy_code_title_query = f"SELECT code, title FROM docs_policy WHERE title LIKE '%{title}%' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
                similar_policy = execute_query(
                    similar_policy_code_title_query)
                similar_policy_code, similar_policy_title = similar_policy[0]

                if result_type == "LLM":
                    return f"FINAL_RESPONSE|No encontré ninguna póliza con el título exacto '{title}'. Sin embargo, encontré una póliza con un título similar: '{similar_policy_title}'. ¿Te refieres a esta póliza?"
                return [{"code": similar_policy_code, "title": similar_policy_title}]

            elif similar_titles_count <= 10:
                similar_policy_codes_and_titles_query = f"SELECT code, title FROM docs_policy WHERE title LIKE '%{title}%' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
                similar_policy_codes_and_titles = execute_query(
                    similar_policy_codes_and_titles_query)
                result_list = [{"code": code, "title": title}
                               for code, title in similar_policy_codes_and_titles]
                if result_type == "LLM":
                    return f"FINAL_RESPONSE|No encontré ninguna póliza con el título exacto '{title}'. Sin embargo, encontré estas pólizas con títulos similares:\n{format_results(similar_policy_codes_and_titles)}\n¿Te refieres a alguna de ellas?"
                return result_list

            else:
                similar_policy_codes_and_titles_query = f"SELECT code, title FROM docs_policy WHERE title LIKE '%{title}%' {'AND is_prohibited = False' if self.filter_prohibited else ''} LIMIT {self.top_k};"
                similar_policy_codes_and_titles = execute_query(
                    similar_policy_codes_and_titles_query)
                result_list = [{"code": code, "title": title}
                               for code, title in similar_policy_codes_and_titles]
                if result_type == "LLM":
                    return f"FINAL_RESPONSE|No encontré ninguna póliza con el título exacto '{title}'. Sin embargo, encontré {similar_titles_count} pólizas con títulos similares. Aquí tienes las {self.top_k} primeras:\n{format_results(similar_policy_codes_and_titles)}\n¿Te refieres a alguna de ellas?"
                return result_list

        elif results_count == 1:
            policy_code_query = f"SELECT content FROM docs_policy WHERE title = '{title}' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
            policy_code_and_title_query = f"SELECT code, title FROM docs_policy WHERE title = '{title}' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
            policy_code, title = execute_query(policy_code_and_title_query)[0]

            policy_content = execute_query(policy_code_query)
            return policy_content if result_type == "LLM" else [{"code": policy_code, "title": title}]

        elif results_count <= 10:
            policy_codes_and_titles_query = f"SELECT code, title FROM docs_policy WHERE title = '{title}' {'AND is_prohibited = False' if self.filter_prohibited else ''};"
            policy_codes_and_titles = execute_query(
                policy_codes_and_titles_query)
            result_list = [{"code": code, "title": title}
                           for code, title in policy_codes_and_titles]
            if result_type == "LLM":
                return f"FINAL_RESPONSE|Encontré las siguientes pólizas con ese título:\n{format_results(policy_codes_and_titles)}\nPor favor, especifica el código de la póliza que deseas consultar."
            return result_list

        else:
            if result_type == "LLM":
                return f"FINAL_RESPONSE|Encontré {results_count} pólizas con ese título. Por favor, especifica el código de la póliza que deseas consultar."

            policy_codes_and_titles_query = f"SELECT code, title FROM docs_policy WHERE title = '{title}' {'AND is_prohibited = False' if self.filter_prohibited else ''} LIMIT {self.top_k};"
            results = execute_query(
                policy_codes_and_titles_query)
            results = sorted(results, key=lambda x: x[0])
            return [{"code": code, "title": title} for code, title in results]

    def is_response_direct(self, response: str):
        response = response.strip()

        # check that response contains SQL|, TITLE_HYBRID_SEARCH| or NEWS_SEARCH|
        action = response.split("|")[0]
        action = action.strip()

        logger.info(f"ACTION: '{action}' - RESPONSE: {response}")
        logger.info(
            f"Action == SQL: {action == 'SQL'} - Action == TITLE_HYBRID_SEARCH: {action == 'TITLE_HYBRID_SEARCH'} - Action == NEWS_SEARCH: {action == 'NEWS_SEARCH'}, Action: {action}")

        if action == "DIRECT_RESPONSE":
            logger.info(f"Response is direct: {response}")
            return True

        elif (action == "SQL") or (action == "TITLE_HYBRID_SEARCH") or (action == "NEWS_SEARCH"):
            logger.info(f"Response is not direct: {response}")
            return False

        elif (action != "SQL") and (action != "TITLE_HYBRID_SEARCH") and (action != "NEWS_SEARCH"):
            logger.info(f"Response is direct: {response}")
            return True

        else:
            return False

    def stream_prompt(self, message: str):
        """
        Stream the response to a given message.

        Args:
            message (str): The input message.

        Yields:
            str: Parts of the response as they are generated.
        """
        message_history = [
            ("system", self.initial_system_prompt),
            *self.transform_history(self.history, output_type="langchain"),
            ("human", "{input}")
        ]
        logger.debug(
            f"(General Agent) {len(message_history)} messages in history.")

        self.qa = ChatPromptTemplate.from_messages(message_history)
        logger.debug(f"(General Agent) QA Prompt: {self.qa}")
        self.chain = self.qa | self.llm | self.str_output_parser

        logger.info(f"(General Agent) Received: {message}")

        # Only stream the response if it is a direct response
        complete_response = ''
        is_direct_response = False
        response_chunks = 0
        for partial_response in self.chain.stream({"input": message}):
            complete_response += partial_response
            response_chunks += 1

            if is_direct_response:
                logger.debug(f"Stream partial response: {partial_response}")
                yield partial_response  # return the rest of the chunks as stream

            if response_chunks == 2:
                is_direct_response = self.is_response_direct(complete_response)
                logger.debug(
                    f"Is direct response: {is_direct_response} - {complete_response}")
                if is_direct_response:
                    logger.debug(
                        f"Stream inital 2 chunks: {complete_response}")
                    cleand_inital_chunks = complete_response.replace(
                        "DIRECT_RESPONSE|", "")
                    yield cleand_inital_chunks  # return the first two chunks

        logger.info(f"COMPLETE RESPONSE: {complete_response}")
        if is_direct_response:
            final_response = complete_response.replace("DIRECT_RESPONSE|", "")
        else:
            final_response = ''
            for chunk in self._process_agent_output_stream(
                user_prompt=message, agent_output=complete_response
            ):
                logger.debug(f"Final response chunk: {chunk}")
                final_response += chunk
                yield chunk

        self.history.append({
            "role": "human",
            "message": message
        })
        self.history.append({
            "role": "ai",
            "message": final_response
        })

        if self.user is not None:
            self.save_chat_history()

        logger.info(f"(General Agent) Final Response: {final_response}")
