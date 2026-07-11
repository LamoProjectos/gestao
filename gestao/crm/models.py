from django.db import models

class Client(models.Model):
    nome = models.CharField('Nome', max_length=200)
    telefone = models.CharField('Telefone', max_length=50, blank=True)
    email = models.EmailField('E-mail', blank=True)
    endereco = models.TextField('Endereço', blank=True)
    nuit = models.CharField('NUIT', max_length=50, blank=True)
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
