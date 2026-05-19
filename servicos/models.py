from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)  # ex: Musculação, Funcional
    descricao = models.TextField(blank=True, null=True)
    duracao_minutos = models.PositiveIntegerField(default=60)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'