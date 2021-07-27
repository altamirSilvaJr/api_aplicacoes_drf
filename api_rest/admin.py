from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']

@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modalidade']

@admin.register(AcaoMovimentacao)
class Acao_movimentacaoAdmin(admin.ModelAdmin):
    list_display = ['acao']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['ativo', 'data_solicitacao', 'quantidade', 'preco_unitario', 'endereco_ip', 'acao']

@admin.register(Carteira)
class CateriaAdmin(admin.ModelAdmin):
    list_display = ['valor_disponivel', 'usuario']

@admin.register(Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = ['valor', 'carteira', 'endereco_ip', 'data_solicitacao']