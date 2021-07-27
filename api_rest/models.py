from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User

# Create your models here.
class Modalidade(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.nome

class Ativo(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    valor_unitario = models.DecimalField(max_digits=50, decimal_places=2)
    def __str__(self):
        return self.nome + " | Valor unitário: R$ " + str(self.valor_unitario)

class AcaoMovimentacao(models.Model):
    acao = models.CharField(max_length=255)
    def __str__(self):
        return self.acao

class Carteira(models.Model):
    valor_disponivel = models.DecimalField(max_digits=50, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_aplicado = models.DecimalField(max_digits=50, decimal_places=2,default=0)
    valor_total = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_disponivel + self.valor_aplicado
        return super(Carteira, self).save()

class Movimentacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    quantidade = models.IntegerField(blank=False)
    preco_unitario = models.DecimalField(max_digits=50, decimal_places=2)
    endereco_ip = models.CharField(max_length=39)
    acao = models.ForeignKey(AcaoMovimentacao, on_delete=models.CASCADE)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)

class Deposito(models.Model):
    valor = models.DecimalField(max_digits=50, decimal_places=2)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)
    endereco_ip = models.CharField(max_length=39)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

class Saque(models.Model):
    valor = models.DecimalField(max_digits=50, decimal_places=2)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)
    endereco_ip = models.CharField(max_length=39)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

class StatusDepositoRetirada(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Aplicacao(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE)
    status_aplicacao = models.BooleanField(default=True)

class Retirada(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE)