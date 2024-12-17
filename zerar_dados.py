from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Remove todos os registros de todos os modelos do projeto'

    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos os registros foram removidos com sucesso.'))