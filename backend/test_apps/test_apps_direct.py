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

# Generate a unique ID
unique_id = uuid4().hex[0:8]

# Set environment variables for Langchain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"poligen-ai-chatbot_app_direct_{unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Load environment variables from .env file
env = dotenv_values()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Downloads\creds.json" 

@fixture()
def qa():
    """
    Fixture for setting up a DatabaseAgent instance with model_name "gemini-1.5-pro".
    Sleeps for 5 seconds to allow setup time before yielding the instance.
    """
    db_agent = DatabaseAgent(model_name="gemini-1.5-pro")
    # Sleep for 5 seconds to allow setup time
    time.sleep(5) 
    yield db_agent 

# List of questions and answers for testing
d_q_a = [
    {'q': 'Que establece el Articulo 7 en la póliza de "PÓLIZA DE ACCIDENTES PERSONALES / REEMBOLSO GASTOS MÉDICOS"? (POL120190177)',
     'a': 'La Póliza se otorga en base a las declaraciones, informaciones y antecedentes proporcionados por el asegurado a solicitud de la Compañía Aseguradora en cumplimiento de la obligación referida en el numeral 1 del artículo anterior, las que deberán prestarse en los formularios o documentos que proporcione la compañía con tal finalidad. Para estos efectos, regirá lo dispuesto en los artículos 525 y 539 del Código de Comercio.'},
    {'q': 'Que establece el Articulo 8 en la póliza de  en la póliza de "SEGURO COLECTIVO COMPLEMENTARIO DE SALUD"? (POL320130223)',
     'a': 'Respecto de las obligaciones del Asegurado, rige lo dispuesto en el Artículo 524 del Código de Comercio.'},
    {'q': 'Que establece el Articulo 19 en la "PÓLIZA DE SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE ACCIDENTE Y ENFERMEDAD"? (POL320150503)',
     'a': 'Los impuestos que se establezcan durante la vigencia de la Póliza y que afecten al presente contrato, serán de cargo del asegurado, salvo que por ley fuesen de cargo de la Compañía Aseguradora.'},
    {'q': 'Que establece el Articulo 3 en la póliza de "SEGURO INDIVIDUAL DE ENFERMEDADES GRAVES"? (POL320160108)',
     'a': 'Solamente se indemnizará una de las enfermedades graves comprendidas en este contrato de seguro diagnosticada durante la vigencia del mismo. El pago del capital asegurado producirá el término de este contrato de seguro.'},     
    {'q': 'Que establece el Articulo 19 en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DERIVADAS DE HOSPITALIZACIÓN QUIRÚRGICA DE EMERGENCIA"? (POL320180100)',
     'a': 'Los impuestos que se establezcan durante la vigencia de la Póliza y que afecten al presente contrato, serán de cargo del asegurado, salvo que por ley fuesen de cargo de la Compañía Aseguradora.'},
    {'q': 'Que establece el Articulo 8 en la prima en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" POL320190074?',
     'a': 'La falta de pago de la prima producirá la terminación del contrato a la expiración del plazo de quince días contado desde la fecha de envío de la comunicación que, con ese objeto, dirija el asegurador al asegurado o Contratante y dará derecho a aquél para exigir que se le pague la prima devengada hasta la fecha de terminación y los gastos de formalización del contrato.'},
    {'q': 'Que establece el Articulo 18 en la póliza de "SEGURO INDIVIDUAL CATASTRÓFICO POR EVENTO"?(POL320200071)',
     'a': 'el contratante o asegurado tendrá la facultad de retractarse dentro del plazo de 10 días, contado desde que reciba la póliza, sin expresión de causa ni cargo alguno, teniendo derecho a la devolución de la prima que hubiere pagado'},
    {'q': 'Que establece el Articulo 9 en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" POL320200214?',
     'a': 'De conformidad al artículo 526 de Código de Comercio, el asegurado titular y/o contratante en su caso, deberá informar al asegurador los hechos o circunstancias que agraven sustancialmente el riesgo declarado y sobrevengan con posterioridad a la celebración del contrato, dentro de los 5 (cinco) días siguientes de haberlos conocido, siempre que por su naturaleza, no hubieren podido ser conocidos de otra forma por el Asegurador.'},
    {'q': 'Que establece el Articulo 8 en la póliza de "SEGURO INDIVIDUAL OBLIGATORIO DE SALUD ASOCIADO A COVID-19"? (POL320210063)',
     'a': 'Tratándose de la cobertura de salud, el Fondo Nacional de Salud y las instituciones de salud previsional, notificarán a la aseguradora respectiva los hechos que puedan constituir o constituyan un siniestro. Tratándose de la cobertura de muerte, el fallecimiento del asegurado deberá ser notificado a la Compañía, de acuerdo con los procedimientos y a través de los medios que esta última disponga para dichos efectos.'},
    {'q': 'Que establece el Articulo 14 en la póliza de "SEGURO PARA PRESTACIONES MÉDICAS DE ALTO COSTO" POL320210210?',
     'a': 'Las cláusulas adicionales que se contraten en forma accesoria con esta póliza complementan o amplían la cobertura establecida en ella, se regirán en todo lo no previsto en el texto de éstas por lo dispuesto en estas Condiciones Generales.'},
]

# Test cases for checking the correct responses

# Test POL120190177
def test_direct_q_a_00_POL120190177(qa: Any):
    """
    Tests the response for the given question related to policy POL120190177.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[0]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[0]["a"], result)

# Test POL320130223
def test_direct_q_a_01_POL320130223(qa: Any):
    """
    Tests the response for the given question related to policy POL320130223.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[1]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[1]["a"], result)

# Test POL320150503
def test_direct_q_a_02_POL320150503(qa: Any):
    """
    Tests the response for the given question related to policy POL320150503.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[2]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[2]["a"], result)

# Test POL320160108    
def test_direct_q_a_03_POL320160108(qa: Any):
    """
    Tests the response for the given question related to policy POL320160108.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[3]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[3]["a"], result)

# Test POL320180100
def test_direct_q_a_04_POL320180100(qa: Any):
    """
    Tests the response for the given question related to policy POL320180100.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[4]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[4]["a"], result)

# Test POL320190074
def test_direct_q_a_05_POL320190074(qa: Any):
    """
    Tests the response for the given question related to policy POL320190074.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[5]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[5]["a"], result)

# Test POL320200071    
def test_direct_q_a_06_POL320200071(qa: Any):
    """
    Tests the response for the given question related to policy POL320200071.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[6]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[6]["a"], result)

# Test POL320200214
def test_direct_q_a_07_POL320200214(qa: Any):
    """
    Tests the response for the given question related to policy POL320200214.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[7]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[7]["a"], result)

# Test POL320210063
def test_direct_q_a_08_POL320210063(qa: Any):
    """
    Tests the response for the given question related to policy POL320210063.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[8]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[8]["a"], result)

# Test POL320210210
def test_direct_q_a_09_POL320210210(qa: Any):
    """
    Tests the response for the given question related to policy POL320210210.
    Asserts that the result matches the expected answer using the distance function.
    """
    result = qa.search(prompt=d_q_a[9]["q"])
    print("LOG PYTEST:", result)
    assert distance(d_q_a[9]["a"], result)
