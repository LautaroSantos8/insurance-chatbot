import time
from typing import Any
from pytest import fixture
from apps.tests.common.eval import distance
from apps.ai.core.agents.news_agent import NewsAgent
from langsmith import Client
from dotenv import dotenv_values
import os
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

# Generate a unique identifier
unique_id = uuid4().hex[0:8]

# Set environment variables for Langchain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"poligen-ai-chatbot_app_news_{unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Load environment variables from .env file
env = dotenv_values()

# Set Google API key
google_api_key = os.getenv("GOOGLE_API_KEY", "")

@fixture(scope='function')
def qa_news():
    """
    Fixture to initialize a NewsAgent instance and provide setup time.
    """
    nw_agent = NewsAgent()   
    time.sleep(5)  # Sleep for 5 seconds to allow setup time
    yield nw_agent 

def test_news_q_a_00_news(qa_news: Any):
    """
    Test to check the response for the regulatory body of insurance policies.
    """
    result = qa_news.search(prompt="Cual es el ente regulador de polizas de seguros")
    print("LOG PYTEST:", result)
    assert ("Comisión para el Mercado Financiero" in result) or distance("Comisión para el Mercado Financiero conmemora cinco años como regulador y supervisor financiero integrado", result)

def test_news_q_a_01_news(qa_news: Any):
    """
    Test to check the response for regulatory modifications regarding FOGAPE and FOGAES.
    """
    result = qa_news.search(prompt="Que modificaciones reglamentarias respecto a FOGAPE y FOGAES")
    print("LOG PYTEST:", result)
    assert distance("La Comisión para el Mercado Financiero (CMF) informa la publicación de tres Circulares con ajustes al Reglamento de administración del Fondo de Garantías para Pequeños Empresarios (FOGAPE) y a los requerimientos de información que la administración del Fondo de Garantías Especiales (FOGAES) debe remitir a la CMF.", result)

def test_news_q_a_02_news(qa_news: Any):
    """
    Test to check the response for fraud and usury crimes.
    """
    result = qa_news.search(prompt="Hay delitos de estafa y usura?")
    print("LOG PYTEST:", result)
    assert ("CMF denunció y alertó presuntos delitos de estafa y usura por entidades que ofrecen créditos" in result) or \
           distance("la Comisión para el Mercado Financiero (CMF) ha denunciado y alertado sobre presuntos delitos de estafa y usura por parte de entidades que ofrecen créditos.", result)

def test_news_q_a_03_news(qa_news: Any):
    """
    Test to check the response for the prohibition of selling certain guarantee or surety insurance policies.
    """
    result = qa_news.searcher_rag(prompt="Cuantas pólizas de seguros de garantía o caución se prohibieron de comercializar recientemente?")
    print("LOG PYTEST:", result)
    assert ("58" in result) or distance("La Comisión para el Mercado Financiero (CMF) informa la prohibición de comercializar 58 pólizas de seguros de garantía o caución a primer requerimiento", result)
