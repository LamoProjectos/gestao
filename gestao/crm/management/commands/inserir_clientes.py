from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '[DEPRECATED] Os clientes são geridos via data migrations.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Este comando está obsoleto. Os dados de seed foram migrados '
            'para crm/migrations/0002_clean_seed_clientes.py'
        ))
