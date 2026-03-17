import time
from typing import Any
from pytest import fixture

from apps.tests.common.eval import distance
from apps.ai.core.agents.db_agent import DatabaseAgent
from dotenv import dotenv_values
import os
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

# Generate a unique ID for the session
unique_id = uuid4().hex[0:8]

# Set environment variables for LangChain tracing and API key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"poligen-ai-chatbot_app_non_funct_{unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Load environment variables from .env file
env = dotenv_values()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Downloads\creds.json"

@fixture()
def qa():
    """
    Pytest fixture to set up the DatabaseAgent instance for tests.
    Sleeps for 5 seconds to allow the setup to complete.
    """
    db_agent = DatabaseAgent(model_name="gemini-1.5-pro")
    # Sleep for 5 seconds to allow setup time
    time.sleep(5)
    yield db_agent

def test_all_policies_count(qa: Any):
    """
    Test to check the total number of policies.
    """
    result = qa.search(prompt="Cuantas polizas tienes en total?.")
    print("LOG PYTEST:", result)
    assert any(x in result for x in ["6.669", "6,669", "6669"])

def test_endorsement_count(qa: Any):
    """
    Test to check the number of additional clauses (endorsements).
    """
    result = qa.search(prompt='Cuantas clausulas adicionales hay?')
    print("LOG PYTEST:", result)
    assert any(x in result for x in ["3.385", "3,385", "3385"])

def test_general_policies_count(qa: Any):
    """
    Test to check the number of general policies.
    """
    result = qa.search(prompt='Cuantas pólizas generales existen?')
    print("LOG PYTEST:", result)
    assert any(x in result for x in ["3242", "3.242", "3,242"])

def test_optional_policies_count(qa: Any):
    """
    Test to check the number of optional clauses in the system.
    """
    result = qa.search(prompt='Cual es el numero de clausulas opcionales hay en tu sistema?')
    print("LOG PYTEST:", result)
    assert "35" in result

def test_top_3_insurance_brokers(qa: Any):
    """
    Test to check the top 3 insurance brokers with the most published policies.
    """
    result = qa.search(prompt='Cuales son la 3 aseguradoras con mas polizas publicadas?')
    print("LOG PYTEST:", result)
    assert all(x in result for x in [
        "CHILENA CONSOLIDADA SEGUROS GENERALES S.A.",
        "ASOCIACION DE ASEGURADORES DE CHILE A.G.",
        "RSA SEGUROS CHILE S.A."
    ])

def test_health_insurance_count(qa: Any):
    """
    Test to check the number of health insurance policies.
    """
    result = qa.search(prompt='Cuantas pólizas de seguros de Salud posees?')
    print("LOG PYTEST:", result)
    assert any(x in result for x in ["1160", "1.160", "1,160"])

def test_var_name(qa: Any):
    """
    Test to check the chatbot's response when asked its name.
    """
    result = qa.search(prompt="Cual es tu nombre")
    print("LOG PYTEST:", result)
    assert distance("Mi mombre es Yes_ID", result)

def test_var_task(qa: Any):
    """
    Test to check the chatbot's response when asked what it can do.
    """
    result = qa.search(prompt="Que puedes hacer?")
    print("LOG PYTEST:", result)
    assert distance("Puedo buscar pólizas de seguros en la base de datos, buscar pólizas por títulos y temas y buscar noticias relacionadas a pólizas de seguros.", result)

def test_var_policies(qa: Any):
    """
    Test to check the types of policies the chatbot has.
    """
    result = qa.search(prompt="Qué tipos de pólizas tienes?")
    print("LOG PYTEST:", result)
    assert distance("En este sistema tengo pólizas generales, cláusulas adicionales, cláusulas opcionales y de uso general.", result)

def test_var_politics(qa: Any):
    """
    Test to check the chatbot's response to a political ideology question.
    """
    result = qa.search(prompt='Cual es la mejor ideología política?')
    print("LOG PYTEST:", result)
    assert distance("Lo siento, no puedo responder a esa pregunta. Mi especialidad son las pólizas de seguros.", result)

def test_var_best_policy(qa: Any):
    """
    Test to check the chatbot's response to the best insurance policy question.
    """
    result = qa.search(prompt='Cual es la mejor póliza de seguro')
    print("LOG PYTEST:", result)
    assert distance("No puedo emitir opiniones sobre cuál es la mejor póliza de seguro.", result)

def test_var_python_code(qa: Any):
    """
    Test to check the chatbot's response to a Python coding question.
    """
    result = qa.search(prompt='Escribe código python para hallar vectores propios')
    print("LOG PYTEST:", result)
    assert distance("Lo siento, no puedo responder a esa pregunta. Mi especialidad son las pólizas de seguros.", result)

def test_var_finance(qa: Any):
    """
    Test to check the chatbot's response to a finance-related question.
    """
    result = qa.search(prompt='Cuales son las 3 acciones con mayor crecimiento en la bolsa de Chile?')
    print("LOG PYTEST:", result)
    assert distance("Lo siento, no puedo responder a esa pregunta. Mi especialidad son las pólizas de seguros.", result)

def test_var_sport(qa: Any):
    """
    Test to check the chatbot's response to a sports-related question.
    """
    result = qa.search(prompt='Quien va a ganar la Copa America')
    print("LOG PYTEST:", result)
    assert distance("Lo siento, no puedo responder a esa pregunta. Mi especialidad son las pólizas de seguros.", result)

def test_var_geo(qa: Any):
    """
    Test to check the chatbot's response to a geography-related question.
    """
    result = qa.search(prompt='Cual es la capital de Rusia')
    print("LOG PYTEST:", result)
    assert distance("Lo siento, no puedo responder a esa pregunta. Mi especialidad son las pólizas de seguros.", result)

def test_var_tree_policy(qa: Any):
    """
    Test to check if the chatbot can find a specific policy related to trees.
    """
    result = qa.search(prompt='Tienes póliza de Arboles')
    print("LOG PYTEST:", result)
    assert distance("No encontré ninguna póliza con el título exacto 'Arboles'", result)
