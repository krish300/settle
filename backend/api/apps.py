from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):  # method just to import the signals
        from . import signals
