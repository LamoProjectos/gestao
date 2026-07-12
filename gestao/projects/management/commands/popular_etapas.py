from django.core.management.base import BaseCommand
from projects.models import TemplateEtapa

ETAPAS_PADRAO = {
    'moradia': [
        ('Levantamento', 1), ('Anteprojeto', 7), ('Projeto Legal', 14),
        ('Projeto Executivo', 21), ('Aprovação', 28), ('Orçamento', 35),
        ('Execução', 42), ('Vistoria', 77), ('Entrega', 84),
    ],
    'ampliacao': [
        ('Levantamento', 1), ('Estudo de Viabilidade', 5), ('Anteprojeto', 10),
        ('Projeto Legal', 17), ('Projeto Executivo', 24), ('Aprovação', 31),
        ('Orçamento', 38), ('Execução', 45), ('Vistoria', 75), ('Entrega', 80),
    ],
    'renovacao': [
        ('Vistoria Inicial', 1), ('Diagnóstico', 3), ('Proposta', 5),
        ('Projeto de Renovação', 10), ('Orçamento', 17), ('Execução', 24),
        ('Vistoria', 54), ('Entrega', 60),
    ],
    'reforma': [
        ('Vistoria Inicial', 1), ('Diagnóstico', 3), ('Projeto de Demolição', 5),
        ('Projeto de Reforma', 10), ('Aprovação', 17), ('Orçamento', 24),
        ('Execução', 31), ('Vistoria', 61), ('Entrega', 67),
    ],
    'salao': [
        ('Estudo de Viabilidade', 1), ('Anteprojeto', 7), ('Projeto Legal', 14),
        ('Projeto Executivo', 21), ('Aprovação', 28), ('Orçamento', 35),
        ('Fundação', 42), ('Estrutura', 56), ('Acabamentos', 70),
        ('Vistoria', 84), ('Entrega', 90),
    ],
    'pool': [
        ('Estudo de Viabilidade', 1), ('Projeto', 5), ('Escavação', 10),
        ('Estrutura', 14), ('Impermeabilização', 21), ('Acabamentos', 28),
        ('Equipamentos', 35), ('Vistoria', 42), ('Entrega', 45),
    ],
    'comercial': [
        ('Estudo de Mercado', 1), ('Anteprojeto', 7), ('Projeto Legal', 14),
        ('Projeto Executivo', 21), ('Aprovação', 28), ('Orçamento', 35),
        ('Execução', 42), ('Vistoria', 77), ('Entrega', 84),
    ],
    'outro': [
        ('Levantamento', 1), ('Proposta', 5), ('Desenvolvimento', 10),
        ('Execução', 17), ('Vistoria', 47), ('Entrega', 54),
    ],
}


class Command(BaseCommand):
    help = 'Popula as etapas padrão para cada tipo de projeto'

    def handle(self, *args, **options):
        TemplateEtapa.objects.all().delete()
        for tipo, etapas in ETAPAS_PADRAO.items():
            for i, (nome, dias) in enumerate(etapas, 1):
                TemplateEtapa.objects.create(
                    tipo_projeto=tipo,
                    ordem=i,
                    nome=nome,
                    dias_apos_inicio=dias,
                )
        self.stdout.write(self.style.SUCCESS(f'Etapas padrão criadas para {len(ETAPAS_PADRAO)} tipos de projeto'))
