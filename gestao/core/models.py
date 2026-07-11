from django.db import models
from django.contrib.auth.models import User

TIPO_NOTIFICACAO = [
    ('info', 'Informativo'),
    ('warning', 'Aviso'),
    ('danger', 'Urgente'),
    ('success', 'Sucesso'),
]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_NOTIFICACAO, default='info')
    mensagem = models.TextField('Mensagem')
    url = models.CharField('Link', max_length=500, blank=True)
    lida = models.BooleanField('Lida', default=False)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criado_em']

    def __str__(self):
        return self.mensagem[:60]

class AgendaEvent(models.Model):
    TIPO_EVENTO = [
        ('etapa', 'Etapa de Projeto'),
        ('pagamento', 'Pagamento'),
        ('marco', 'Marco do Projeto'),
    ]

    projeto = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_EVENTO, default='etapa')
    data = models.DateField('Data')
    data_fim = models.DateField('Data Fim', null=True, blank=True)
    concluido = models.BooleanField('Concluído', default=False)
    url = models.CharField('Link', max_length=500, blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Evento de Agenda'
        verbose_name_plural = 'Eventos de Agenda'
        ordering = ['data']

    def __str__(self):
        return self.titulo
