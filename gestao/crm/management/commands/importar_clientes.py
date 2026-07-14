from django.core.management.base import BaseCommand
from crm.models import Client


CLIENTES = [
    {
        'nome': 'Venestâncio Tomás Cossa',
        'telefone': '84 763 8748',
        'email': 'venestc50@gmail.com',
        'endereco': 'Maputo, Boane',
        'observacoes': 'Cotação LP-2026-005 — 10.000 MZN',
    },
    {
        'nome': 'Zelio Amandio da Silva Guirrugo',
        'telefone': '86 308 5285',
        'email': 'zguirrugo@gmail.com',
        'endereco': 'Maputo, Mulotane',
        'observacoes': 'Cotação LP-2026-007 — 12.500 MZN',
    },
    {
        'nome': 'Sebastião Cossa',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Remodelação',
    },
    {
        'nome': 'Pene Vasconcelos',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Moradia Tipo 3',
    },
    {
        'nome': 'Manuel Chimututo',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': '',
    },
]


class Command(BaseCommand):
    help = 'Insere os clientes reais da LamoProjectos'

    def handle(self, *args, **options):
        criados = 0
        existentes = 0

        for data in CLIENTES:
            _, created = Client.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'telefone': data.get('telefone', ''),
                    'email': data.get('email', ''),
                    'endereco': data.get('endereco', ''),
                    'observacoes': data.get('observacoes', ''),
                },
            )
            if created:
                criados += 1
                self.stdout.write(f'  ✓ {data["nome"]}')
            else:
                existentes += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n{criados} cliente(s) criado(s), {existentes} já existente(s).'
        ))
