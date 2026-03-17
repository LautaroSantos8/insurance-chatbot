from apps.ai.core.agents.news_agent import NewsAgent
from apps.ai.core.agents.general_agent import GeneralAgent
from django.test import TestCase


class TestDBRetrieval(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_agent = GeneralAgent(
            model_name="gemini-1.5-pro",
            reset_history=True
        )

    def test_all_policies_count(self):
        result = self.general_agent.search(
            prompt="Cuantas polizas tienes en total?."
        )
        self.assertTrue(
            any(x in result for x in ["6.669", "6,669", "6669"]),
        )

    def test_endorsement_count(self):
        result = self.general_agent.search(
            prompt='Cuantas clausulas adicionales hay?'
        )
        self.assertTrue(
            any(x in result for x in ["3.385", "3,385", "3385"]),
        )

    def test_general_policies_count(self):
        result = self.general_agent.search(
            prompt='Cuantas pólizas generales existen?'
        )
        self.assertTrue(
            any(x in result for x in ["3242", "3.242", "3,242"]),
        )

    def test_optional_policies_count(self):
        result = self.general_agent.search(
            prompt='Cual es el numero de clausulas opcionales hay en tu sistema?'
        )
        self.assertIn("35", result)

    def test_top_3_insurance_brokers(self):
        result = self.general_agent.search(
            prompt='Cuales son la 3 aseguradoras con mas polizas publicadas?'
        )
        self.assertTrue(
            all(x in result for x in [
                "CHILENA CONSOLIDADA SEGUROS GENERALES S.A.",
                "ASOCIACION DE ASEGURADORES DE CHILE A.G.",
                "RSA SEGUROS CHILE S.A."
            ]),
        )

    def test_health_insurance_count(self):
        result = self.general_agent.search(
            prompt='Cuantas pólizas de seguros de salud posees?'
        )
        self.assertTrue(
            any(x in result for x in ["1160", "1.160", "1,160"]),
        )

    def test_life_insurance_count(self):
        result = self.general_agent.search(
            prompt='Cuantas pólizas de seguros de vida posees?'
        )
        self.assertTrue(
            any(x in result for x in ["1.123", "1123", "1,123"]),
        )


class TestHybridSearch(TestCase):
    def test_all_policies_count(self):
        result = self.general_agent.search(
            prompt="Cuantas polizas tienes en total?."
        )
        self.assertTrue(
            any(x in result for x in ["6.669", "6,669", "6669"]),
        )


news_agent = NewsAgent()
general_agent = GeneralAgent()


# Testing - General Agent DB Retrieval
class TestDBRetrieval(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_agent = GeneralAgent(
            model_name="gemini-1.5-pro",
            reset_history=True
        )

    def test_all_policies_count(self):
        result = self.general_agent.search(
            prompt="Cuantas polizas tienes en total?."
        )
        self.assertTrue(
            any(x in result for x in ["6.669", "6,669", "6669"]),
        )

    def test_endorsement_count(self):
        result = self.general_agent.search(
            prompt='Cuantas clausulas adicionales hay?'
        )
        self.assertTrue(
            any(x in result for x in ["3.385", "3,385", "3385"]),
        )

    # Resto de ejempos en apps/ai/tests.py


# Testing - General Agent Ouot of context questions
class TestOutOfContextQuestionGeneralAgent(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_agent = GeneralAgent(
            model_name="gemini-1.5-pro",
            reset_history=True
        )

    def test_out_of_context_question(self):
        result = self.general_agent.search(
            prompt="Cual es la capital de Francia?"
        )
        self.assertIn("No tengo un nombre", result)

        ...  # Y mas así


# Testing - General Agent Direct Responses
class TestDirectResponsesGeneralAgent(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_agent = GeneralAgent(
            model_name="gemini-1.5-pro",
            reset_history=True
        )

    def test_direct_response(self):
        result = self.general_agent.search(
            prompt="Cual es tu nombre?"
        )
        self.assertIn("Soy un agente de inteligencia artificial", result)

        ...  # Y mas así


# Testing - News Agent
class TestNewsAgent(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.news_agent = NewsAgent()

    def test_news_search(self):
        pass

    # hay que definir bien como


# Testing - Search engine (quick search)
class TestQuickSearch(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.general_agent = GeneralAgent(
            model_name="gemini-1.5-pro",
            reset_history=True
        )

    def test_quick_search(self):
        result: str = self.general_agent.hybrid_title_search(
            prompt="Tienes polizas de manzanas?",
            result_type="LLM"
        )
        top_k = self.general_agent.top_k

        assert result.startswith(
            f"""FINAL_RESPONSE|No encontré ninguna póliza con el título exacto 'MANZANAS' Sin embargo, aquí tienes las {top_k} pólizas más similares que encontré:""")

        # así con varios ejemplos. Las respuestas están en apps/ai/core/agents/general_agent.py

    # tambien probar con retyrb:type="JSON"
    def search_engine_json(self):
        result: str = self.general_agent.hybrid_title_search(
            prompt="Tienes polizas de seguros medios?",
            result_type="JSON"
        )

        assert result == []  # obtener el JSON de respuestas de la búsqueda y comparar
