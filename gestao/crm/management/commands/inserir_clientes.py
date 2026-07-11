from django.core.management.base import BaseCommand
from crm.models import Client

CLIENTES = [
    {
        'nome': 'Venestâncio Tomás Cossa',
        'telefone': '84 763 8748',
        'email': 'venestc50@gmail.com',
        'endereco': 'Boane',
        'observacoes': 'Cotação LP-2026-005 — 10.000 MZN',
    },
    {
        'nome': 'Inoque João Cesar',
        'telefone': '',
        'email': '',
        'endereco': 'Matola',
        'observacoes': '',
    },
    {
        'nome': 'Manuel Chimututo',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': '',
    },
    {
        'nome': 'Família Guava',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Ampliação + Pool',
    },
    {
        'nome': 'Matlemele',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Reforma',
    },
    {
        'nome': '2ª Rotunda',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Renovação',
    },
    {
        'nome': 'Katembe',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Moradia',
    },
    {
        'nome': 'Muhalaze',
        'telefone': '',
        'email': '',
        'endereco': '',
        'observacoes': 'Salão de Eventos',
    },
]


class Command(BaseCommand):
    help = 'Insere os clientes existentes no sistema'

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
