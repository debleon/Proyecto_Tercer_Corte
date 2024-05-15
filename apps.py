from django.apps import AppConfig

class GestionDeNominaConfig(AppConfig):
    name = 'gestion_de_nomina'

    def ready(self):
        import gestion_de_nomina.celery_beat
