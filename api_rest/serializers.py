from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
        ]
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        carteira = Carteira.objects.create(
            valor_disponivel = 0.00,
            usuario = user
        )
        carteira.save()
        return user

class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = [
            'nome',
            'modalidade',
            'valor_unitario'
        ]

class AcaoMovimentacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcaoMovimentacao
        fields = [
            'acao'
        ]

class MovimentacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movimentacao
        fields = [
            'ativo',
            'data_solicitacao',
            'quantidade',
            'acao',
        ]

class CarteiraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carteira
        fields = [
            'valor_disponivel',
            'usuario',
            'valor_aplicado',
            'valor_total',
        ]

class DepositoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Deposito
        fields = [
            'valor',
            'data_solicitacao'
        ]

class SaqueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Saque
        fields = [
            'valor',
            'data_solicitacao'
        ]