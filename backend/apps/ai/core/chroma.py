from dotenv import dotenv_values
from common.logger import logger
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient, Collection
from typing import Dict, List, Union
from chromadb import QueryResult
from config.paths import CHROMA_SQLITE_DB_DIR
env = dotenv_values()


class ChromaManager:
    """
    Singleton class to manage ChromaDB collections and operations.

    Attributes:
        _instance (ChromaManager): The singleton instance of the class.
        client (PersistentClient): The ChromaDB client.
        collections (List[str]): The list of collection names.
        embeddings_model (SentenceTransformer): The SentenceTransformer model for embeddings.
    """
    _instance = None

    def __new__(cls) -> 'ChromaManager':
        if not cls._instance:
            cls._instance = super(ChromaManager, cls).__new__(cls)
            cls.client = PersistentClient(path=CHROMA_SQLITE_DB_DIR)
            cls.collections = ['documents', 'articles', 'chunks']
            cls.embeddings_model = SentenceTransformer(
                'sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

            existing_collections = [
                col.name for col in cls.client.list_collections()]
            logger.debug(f"Found existing collections: {existing_collections}")

            for collection in cls.collections:
                if collection not in existing_collections:
                    logger.debug(
                        f"Collections {collection} not found. in {existing_collections}")
                    cls.client.create_collection(name=collection)
                    logger.debug(f"Collection {collection} created.")

        return cls._instance

    def reset_all_collections(self) -> None:
        """
        Reset all collections by deleting and recreating them.
        """
        for collection in self.collections:
            self.client.delete_collection(collection)
            self.client.create_collection(name=collection)
            logger.debug(f"Collection {collection} reset.")

    def reset_collection(self, collection: str) -> None:
        """
        Reset a specific collection by deleting and recreating it.

        Args:
            collection (str): The name of the collection to reset.
        """
        self.client.delete_collection(collection)
        self.client.create_collection(name=collection)
        logger.debug(f"Collection {collection} reset.")

    def get_collection(self, collection: str) -> Collection:
        """
        Get a specific collection.

        Args:
            collection (str): The name of the collection to get.

        Returns:
            Collection: The requested collection.
        """
        return self.client.get_collection(collection)

    def similarity_search(self, collection_name: str, query: str, top_k: int = 10, metadata_filters: dict = {"is_prohibited": False}) -> QueryResult:
        """
        Perform a similarity search in a specific collection.

        Args:
            collection_name (str): The name of the collection to search in.
            query (str): The query string.
            top_k (int, optional): The number of top results to return. Defaults to 10.
            metadata_filters: (dict, optional): The metadata filters to apply. Defaults to {"is_prohibited": False}.

        Returns:
            QueryResult: The search result.

        Raises:
            ValueError: If the collection does not exist.
        """
        collection = self.get_collection(collection_name)
        if not collection:
            raise ValueError(f"Invalid collection type: {collection_name}")

        query_embedding = self.embeddings_model.encode([query])

        return collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where=metadata_filters
        )

    def add_entry(self, collection_name: str, pol_id: str, str_embedding: str, metadata: Dict = {}) -> None:
        """
        Add an entry to a specific collection.

        Args:
            collection_name (str): The name of the collection to add the entry to.
            pol_id (str): The policy ID.
            str_embedding (str): The string to embed.
            metadata (Dict, optional): The metadata to associate with the entry. Defaults to {}.

        Raises:
            ValueError: If the collection does not exist.
        """
        collection = self.get_collection(collection_name)
        if not collection:
            raise ValueError(f"Invalid collection type: {collection_name}")

        embedding = self.embeddings_model.encode([str_embedding])

        collection.upsert(
            ids=pol_id,
            embeddings=embedding,
            metadatas=metadata
        )

    def id_search(self, id: str, collection_name: str = 'documents') -> Union[Dict, None]:
        """
        Search for a document by ID in a specific collection.

        Args:
            id (str): The ID of the document to search for.
            collection_name (str, optional): The name of the collection to search in. Defaults to 'documents'.

        Returns:
            Dict: The document if found, None otherwise.

        Raises:
            ValueError: If the collection does not exist.
        """
        collection = self.get_collection(collection_name)
        if not collection:
            raise ValueError(f"Invalid collection type: {collection_name}")

        return collection.get_document(id=id)
