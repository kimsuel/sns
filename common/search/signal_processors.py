from django_elasticsearch_dsl.signals import RealTimeSignalProcessor
from django_elasticsearch_dsl.registries import registry


class MySignalProcessor(RealTimeSignalProcessor):
    def handle_save(self, instance, **kwargs):
        registry.update(instance)

    def handle_delete(self, instance, **kwargs):
        registry.delete(instance)
