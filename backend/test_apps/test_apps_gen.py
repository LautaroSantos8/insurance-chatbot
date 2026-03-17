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

# Generate a unique identifier
unique_id = uuid4().hex[0:8]

# Set environment variables for LangChain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"poligen-ai-chatbot_app_general_{unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Load environment variables from a .env file
env = dotenv_values()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Downloads\\creds.json"

@fixture()
def qa():
    """
    Fixture to initialize the DatabaseAgent for testing.
    
    Yields:
        DatabaseAgent: Initialized database agent for querying.
    """
    db_agent = DatabaseAgent(model_name="gemini-1.5-pro")
    # Sleep for 5 seconds to allow setup time
    time.sleep(5)
    yield db_agent

# List of question and answer pairs for testing
q_a = [
    {
        'q': 'Que se establece referido al domicilio especial en la póliza de "PÓLIZA DE ACCIDENTES PERSONALES / REEMBOLSO GASTOS MÉDICOS"? (POL120190177)',
        'a': 'las partes señalan como domicilio especial el que aparece detallado con tal carácter en las Condiciones Particulares de la Póliza'
    },
    {
        'q': 'A quienes se consideran asegurados de esta póliza de "SEGURO COLECTIVO COMPLEMENTARIO DE SALUD"? (POL320130223)',
        'a': 'a las personas que, habiendo solicitado su incorporación a la póliza y cumpliendo con los requisitos de asegurabilidad establecidos en las Condiciones Particulares, hayan sido ceptados por la compañía de seguros y se encuentren incluidos en las Condiciones Particulares de la póliza.'
    },
    {
        'q': 'Cuales son las contribuciones e impuestos de la póliza de "PÓLIZA DE SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE ACCIDENTE Y ENFERMEDAD"? (POL320150503)',
        'a': 'Los impuestos que se establezcan durante la vigencia de la Póliza y que afecten al presente contrato, serán de cargo del asegurado, salvo que por ley fuesen de cargo de la Compañía Aseguradora.'
    },
    {
        'q': 'Que se establece sobre el cancer en la póliza de "SEGURO INDIVIDUAL DE ENFERMEDADES GRAVES"? (POL320160108)',
        'a': 'Para efectos de este contrato de seguro se entiende por cáncer la enfermedad neoplásica que se manifiesta por la presencia de un tumor maligno. Este contrato de seguro no otorga cobertura al cáncer a la piel que no sea melanoma maligno y a los tumores en presencia de un virus de inmunodeficiencia adquirida SIDA'
    },
    {
        'q': 'Como es el calculo de los gastos reembolsables póliza de "SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE HOSPITALIZACIÓN QUIRÚRGICA DE EMERGENCIA"? (POL320180100)',
        'a': 'el procedimiento de cálculo de los Gastos Reembolsables considerará únicamente los Gastos Efectivamente Incurridos, esto es, la diferencia entre el monto total de los Gastos Médicos Razonables y Acostumbrados a causa de un Evento y aquellas cantidades que sean restituidas, aportadas, bonificadas o reembolsadas al Asegurado por instituciones'
    },
    {
        'q': 'Que ocurre con la falta de pago de la prima en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" POL320190074?',
        'a': 'La falta de pago de la prima producirá la terminación del contrato a la expiración del plazo de quince días contado desde la fecha de envío de la comunicación que, con ese objeto, dirija el asegurador al asegurado o Contratante y dará derecho a aquél para exigir que se le pague la prima devengada hasta la fecha de terminación y los gastos de formalización del contrato.'
    },
    {
        'q': 'El asegurado tiene la facultad de retractarse en la póliza de "SEGURO INDIVIDUAL CATASTRÓFICO POR EVENTO"?(POL320200071)',
        'a': 'el contratante o asegurado tendrá la facultad de retractarse dentro del plazo de 10 días, contado desde que reciba la póliza, sin expresión de causa ni cargo alguno, teniendo derecho a la devolución de la prima que hubiere pagado'
    },
    {
        'q': 'En que consiste el equipo medico durable de la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" POL320200214?',
        'a': 'El equipo médico durable (EMD) provee beneficios terapéuticos al individuo y le permite realizar tareas que de otra forma y debido a ciertas condiciones médicas o enfermedades no podría realizar.'
    },
    {
        'q': 'Cuales son las condiciones en el riesgo de muerte de la póliza de "SEGURO INDIVIDUAL OBLIGATORIO DE SALUD ASOCIADO A COVID-19"? (POL320210063)',
        'a': 'En caso de fallecimiento cuya causa básica de defunción sea COVID-19, según la codificación oficial establecida por el Ministerio de Salud, se pagará un monto equivalente a 180 unidades de fomento.'
    },
    {
        'q': 'Que se establece sobre las clausulas adicionales en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" (POL320210210)?',
        'a': 'Las cláusulas adicionales que se contraten en forma accesoria con esta póliza complementan o amplían la cobertura establecida en ella, se regirán en todo lo no previsto en el texto de éstas por lo dispuesto en estas Condiciones Generales.'
    }
]

# Test functions for good Q&A pairs
def test_good_q_a_00_POL120190177(qa: Any):
    """
    Test RAG for POL120190177.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[0]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[0]["a"], result)

def test_good_q_a_01_POL320130223(qa: Any):
    """
    Test RAG for POL320130223.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[1]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[1]["a"], result)

def test_good_q_a_02_POL320150503(qa: Any):
    """
    Test RAG for POL320150503.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[2]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[2]["a"], result)

def test_good_q_a_03_POL320160108(qa: Any):
    """
    Test RAG for POL320160108.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[3]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[3]["a"], result)

def test_good_q_a_04_POL320180100(qa: Any):
    """
    Test RAG for POL320180100.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[4]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[4]["a"], result)

def test_good_q_a_05_POL320190074(qa: Any):
    """
    Test RAG for POL320190074.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[5]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[5]["a"], result)

def test_good_q_a_06_POL320200071(qa: Any):
    """
    Test RAG for POL320200071.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[6]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[6]["a"], result)

def test_good_q_a_07_POL320200214(qa: Any):
    """
    Test RAG for POL320200214.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[7]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[7]["a"], result)

def test_good_q_a_08_POL320210063(qa: Any):
    """
    Test RAG for POL320210063.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[8]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[8]["a"], result)

def test_good_q_a_09_POL320210210(qa: Any):
    """
    Test RAG for POL320210210.
    
    Args:
        qa (Any): The DatabaseAgent fixture.
    """
    result = qa.search(prompt=q_a[9]["q"])
    print("LOG PYTEST:", result)
    assert distance(q_a[9]["a"], result)
