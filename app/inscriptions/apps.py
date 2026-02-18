from django.apps import AppConfig


class InscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inscriptions'

    def ready(self):
        # Cette ligne est cruciale pour que le signal soit "écouté"
        import inscriptions.signals

