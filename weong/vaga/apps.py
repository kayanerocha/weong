from django.apps import AppConfig

class VagaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vaga'

    def ready(self):
        import vaga.signals
