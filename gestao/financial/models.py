from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from crm.models import Client
from projects.models import Project

STATUS_QUOTE = [
    ('pendente', 'Pendente'),
    ('aprovada', 'Aprovada'),
    ('recusada', 'Recusada'),
]

STATUS_PAGAMENTO = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('atrasado', 'Atrasado'),
]

CATEGORIAS_CAIXA = [
    ('honorarios', 'Honorários'),
    ('adiantamento', 'Adiantamento'),
    ('pagamento_projecto', 'Pagamento de Projecto'),
    ('outra_entrada', 'Outra Entrada'),
    ('material', 'Material'),
    ('servicos', 'Serviços'),
    ('salarios', 'Salários'),
    ('impostos', 'Impostos'),
    ('transporte', 'Transporte'),
    ('equipamento', 'Equipamento'),
    ('outra_saida', 'Outra Saída'),
]

FORMA_PAGAMENTO = [
    ('transferencia', 'Transferência Bancária'),
    ('deposito', 'Depósito'),
    ('dinheiro', 'Dinheiro'),
    ('mpesa', 'M-Pesa'),
    ('emola', 'E-Mola'),
]

class Quote(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cotacoes', verbose_name='Cliente')
    projeto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cotacoes', verbose_name='Projeto', null=True, blank=True)
    numero = models.CharField('Nº Cotação', max_length=20, unique=True)
    data_emissao = models.DateField('Data de Emissão', auto_now_add=True)
    valor_total = models.DecimalField('Valor Total (MZN)', max_digits=12, decimal_places=2)
    valor_primeira_prestacao = models.DecimalField('1ª Prestação (MZN)', max_digits=12, decimal_places=2)
    valor_segunda_prestacao = models.DecimalField('2ª Prestação (MZN)', max_digits=12, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=STATUS_QUOTE, default='pendente')
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.numero} - {self.cliente.nome}'

    def saldo_pendente(self):
        total_pago = sum(p.valor for p in self.pagamentos.filter(status='pago'))
        return self.valor_total - total_pago

class Payment(models.Model):
    cotacao = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='pagamentos', verbose_name='Cotação')
    prestacao = models.PositiveSmallIntegerField('Prestação')
    valor = models.DecimalField('Valor (MZN)', max_digits=12, decimal_places=2)
    data_vencimento = models.DateField('Data de Vencimento')
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_PAGAMENTO, default='pendente')
    metodo = models.CharField('Método', max_length=50, blank=True)
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['prestacao']

    def __str__(self):
        return f'{self.cotacao.numero} - {self.prestacao}ª Prestação'


class CashFlow(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField('Categoria', max_length=30, choices=CATEGORIAS_CAIXA)
    valor = models.DecimalField('Valor (MZN)', max_digits=12, decimal_places=2)
    data = models.DateField('Data')
    descricao = models.TextField('Descrição')
    cliente = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    cotacao = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cotação')
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=20, choices=FORMA_PAGAMENTO, blank=True)
    documento = models.CharField('Nº Documento', max_length=50, blank=True, help_text='Nº de recibo, transferência, etc.')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Movimento de Caixa'
        verbose_name_plural = 'Movimentos de Caixa'
        ordering = ['-data', '-criado_em']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.valor} MZN ({self.data})'


class CompanySettings(models.Model):
    assinatura = models.ImageField('Assinatura', upload_to='config/', blank=True, null=True)
    nome_administrador = models.CharField('Nome do Administrador', max_length=200, default='Cleiton Simião Ndona')
    cargo = models.CharField('Cargo', max_length=200, default='Administrador')
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Configuração da Empresa'
        verbose_name_plural = 'Configurações da Empresa'

    def __str__(self):
        return 'Configurações da Empresa'


@receiver(post_save, sender=Payment)
def notificar_pagamento(sender, instance, created, **kwargs):
    from core.models import Notification
    from django.contrib.auth.models import User
    from datetime import datetime

    hoje = date.today()
    if instance.status == 'pendente' and instance.data_vencimento:
        vencimento = instance.data_vencimento
        if isinstance(vencimento, str):
            vencimento = datetime.strptime(vencimento, '%Y-%m-%d').date()
        if vencimento <= hoje + timedelta(days=5):
            msg = f'Pagamento {instance.prestacao}ª prestação de {instance.cotacao.numero} vence em {instance.data_vencimento}'
            url = f'/financial/cotacoes/{instance.cotacao.id}/'
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                if not Notification.objects.filter(mensagem=msg, user=admin, lida=False).exists():
                    Notification.objects.create(user=admin, tipo='warning', mensagem=msg, url=url)
