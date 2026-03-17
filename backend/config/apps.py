from django.apps import AppConfig
from common.logger import logger
from utils.validators import validate_environment


class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        validate_environment()
        from apps.ai.core.chroma import ChromaManager
        self.chroma_manager_instance = ChromaManager()
