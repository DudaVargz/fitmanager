from django.db import models
from clientes.models import Cliente
from profissionais.models import Profissional
from servicos.models import Servico

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente} - {self.data_hora.strftime("%d/%m/%Y %H:%M")}'

    class Meta:
        ordering = ['data_hora']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'