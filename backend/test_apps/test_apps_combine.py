import time
from typing import Any
from pytest import fixture

from apps.tests.common.eval import distance
from apps.tests.common.tools import extract_result
from apps.ai.core.agents.db_agent import DatabaseAgent
from dotenv import dotenv_values
import os
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

# Generate a unique identifier for the project
unique_id = uuid4().hex[0:8]

# Set environment variables for LangChain API
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"poligen-ai-chatbot_app_combine_{unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Load environment variables from .env file
env = dotenv_values()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Downloads\creds.json" 

@fixture()
def qa():
    """
    Pytest fixture to set up the DatabaseAgent.

    Yields:
        DatabaseAgent: An instance of DatabaseAgent configured with the model "gemini-1.5-pro".
    """
    db_agent = DatabaseAgent(model_name="gemini-1.5-pro")

    # Sleep for 5 seconds to allow setup time
    time.sleep(5) 
    yield db_agent 

# List of question and answer pairs for testing
c_q_a = [
    {
        'q': 'Puedes combinar el Articulo 7 en la "PÓLIZA DE SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE ACCIDENTE Y ENFERMEDAD"(POL320150503) y el Articulo 7 de la "PÓLIZA DE SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE HOSPITALIZACIÓN QUIRÚRGICA DE EMERGENCIA"(POL320180100)?',
        'a': 'La Póliza se otorga en base a las declaraciones, informaciones y antecedentes proporcionados por el asegurado a solicitud de la Compañía Aseguradora en cumplimiento de la obligación referida en el numeral 1 del artículo anterior, las que deberán prestarse en los formularios o documentos que proporcione la compañía con tal finalidad. Para estos efectos, regirá lo dispuesto en los artículos 525 y 539 del Código de Comercio.'
    },
    {
        'q': 'Puedes combinar el Articulo 13 en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO"(POL320190074) y el articulo 18 de la poliza "SEGURO PARA PREstaciones MÉDICAS DE ALTO COSTO"(POL320200214)?',
        'a': '''Cualquier dificultad que se suscite entre el asegurado, el contratante o el beneficiario, según corresponda, y el asegurador, sea en relación con la validez o ineficacia del contrato de seguro, o con motivo de la interpretación o aplicación de sus condiciones generales o particulares, su cumplimiento o incumplimiento, o sobre la procedencia o el monto de una indemnización reclamada al amparo del mismo, será resuelta en los términos establecidos en el Artículo 543 del Código de Comercio.
        Todo lo anterior se entiende sin perjuicio del derecho que tiene el Asegurado de recurrir siempre ante el tribunal competente en ejercicio de sus derechos de consumidor conforme a la Ley 19.496.
        No obstante lo estipulado precedentemente, el asegurado, el contratante o beneficiario, según corresponda, podrá, por sí solo y en cualquier momento, someter al arbitraje de la Comisión del Mercado Financiero las dificultades que se susciten con la compañía cuando el monto de los daños reclamados no sea superior a 120 Unidades de Fomento, de conformidad a lo dispuesto en la letra i) del artículo 3º del Decreto con Fuerza de Ley Nº 251, de Hacienda, de 1931.
        Si los interesados no se pusieren de acuerdo en la persona del árbitro, éste será designado por la justicia ordinaria y, en tal caso, el árbitro tendrá las facultades de arbitrador en cuanto al procedimiento, debiendo dictar sentencia conforme a derecho. En ningún caso podrá designarse en el contrato de seguro, de antemano, a la persona del árbitro.
        En las disputas entre el asegurado y el Asegurador que surjan con motivo de un siniestro cuyo monto sea inferior a 10.000 unidades de fomento, el asegurado podrá optar por ejercer su acción ante la justicia ordinaria.'''
    },
    {
        'q': 'Puedes combinar sobre domicilio en el Articulo 19 en el "SEGURO INDIVIDUAL CATASTRÓFICO POR EVENTO"(POL320200071) y el Articulo 19 del "SEGURO INDIVIDUAL DE ENFERMEDADES GRAVES"(POL320160108)?',
        'a': 'Para todos los efectos legales del presente contrato de seguro, las partes señalan como domicilio especial el que aparece detallado con tal carácter en las Condiciones Particulares de la póliza.'
    },
]

def test_combine_POL320150503_POL320180100(qa: Any):
    """
    Tests the combination of Article 7 in POL320150503 and POL320180100.

    Args:
        qa (Any): The DatabaseAgent fixture.

    Asserts:
        Checks if the extracted result matches the expected answer using distance function.
    """
    result = qa.search(prompt=c_q_a[0]["q"])
    result = extract_result(result, end="\n \n  \n  \n")
    print("LOG PYTEST:", result)
    assert distance(c_q_a[0]["a"], result)

def test_combine_POL320190074_POL320200214(qa: Any):
    """
    Tests the combination of Article 13 in POL320190074 and Article 18 in POL320200214.

    Args:
        qa (Any): The DatabaseAgent fixture.

    Asserts:
        Checks if the extracted result matches the expected answer using distance function.
    """
    result = qa.search(prompt=c_q_a[1]["q"])
    result = extract_result(result, end="\n \n  \n  \n")
    print("LOG PYTEST:", result)
    assert distance(c_q_a[1]["a"], result)

def test_combine_POL320200071_POL320160108(qa: Any):
    """
    Tests the combination of Article 19 in POL320200071 and POL320160108.

    Args:
        qa (Any): The DatabaseAgent fixture.

    Asserts:
        Checks if the extracted result matches the expected answer using distance function.
    """
    result = qa.search(prompt=c_q_a[2]["q"])
    result = extract_result(result, end="\n \n  \n  \n")
    print("LOG PYTEST:", result)
    assert distance(c_q_a[2]["a"], result)

