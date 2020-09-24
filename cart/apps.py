from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'cart'

    def ready(self):
        """ import signals so signals module/listeners work """
        import cart.signals
