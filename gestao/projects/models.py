from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from crm.models import Client

TIPO_PROJETO = [
    ('moradia', 'Moradia'),
    ('ampliacao', 'Ampliação'),
    ('renovacao', 'Renovação'),
    ('reforma', 'Reforma'),
    ('salao', 'Salão de Eventos'),
    ('pool', 'Pool Familiar'),
    ('comercial', 'Comercial'),
    ('outro', 'Outro'),
]

STATUS_PROJETO = [
    ('proposta', 'Proposta'),
    ('aprovado', 'Aprovado'),
    ('em_andamento', 'Em Andamento'),
    ('concluido', 'Concluído'),
    ('cancelado', 'Cancelado'),
]

class Project(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projetos', verbose_name='Cliente')
    nome = models.CharField('Nome do Projeto', max_length=200)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_PROJETO)
    status = models.CharField('Status', max_length=20, choices=STATUS_PROJETO, default='proposta')
    descricao = models.TextField('Descrição', blank=True)
    valor_total = models.DecimalField('Valor Total (MZN)', max_digits=12, decimal_places=2, default=0)
    data_inicio = models.DateField('Data de Início', null=True, blank=True)
    data_entrega = models.DateField('Data de Entrega', null=True, blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.nome} - {self.cliente.nome}'

class ProjectStage(models.Model):
    projeto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='etapas', verbose_name='Projeto')
    ordem = models.PositiveIntegerField('Ordem')
    nome = models.CharField('Etapa', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    data_prevista = models.DateField('Data Prevista', null=True, blank=True)
    data_conclusao = models.DateField('Data de Conclusão', null=True, blank=True)
    concluida = models.BooleanField('Concluída', default=False)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.ordem}. {self.nome}'


@receiver(post_save, sender=ProjectStage)
def notificar_etapa(sender, instance, created, **kwargs):
    from core.models import Notification
    from django.contrib.auth.models import User

    hoje = date.today()
    if not instance.concluida and instance.data_prevista:
        if instance.data_prevista <= hoje + timedelta(days=5):
            msg = f'Etapa "{instance.nome}" do projeto "{instance.projeto.nome}" prevista para {instance.data_prevista}'
            url = f'/projects/{instance.projeto.id}/'
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                    Notification.objects.create(user=admin, tipo='warning', mensagem=msg, url=url)
