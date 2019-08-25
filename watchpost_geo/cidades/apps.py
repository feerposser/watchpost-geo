from django.apps import AppConfig


class CidadesConfig(AppConfig):
    name = 'cidades'

    def ready(self):
        import cidades.signals