from django.core.management.base import BaseCommand
from core.signals import (
    verificar_pagamentos_proximos,
    verificar_pagamentos_atrasados,
    verificar_etapas_proximas,
    verificar_etapas_atrasadas,
)


class Command(BaseCommand):
    help = 'Verifica pagamentos e etapas próximos/atrasados e cria notificações. '
    'Pronto para agendamento (cron / Render scheduler).'

    def handle(self, *args, **options):
        verificar_pagamentos_proximos()
        verificar_pagamentos_atrasados()
        verificar_etapas_proximas()
        verificar_etapas_atrasadas()
        self.stdout.write(self.style.SUCCESS('Verificação de alertas concluída.'))
