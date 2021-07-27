from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status

from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import *
from . serializers import *

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CarteiraViewSet(mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
    queryset = Carteira.objects.all()
    serializer_class = CarteiraSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.usuario.id:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'Erro' : 'Você não está autorizado a ver essa carteira'})

class DepositoViewSet(viewsets.ModelViewSet):
    queryset = Deposito.objects.all()
    serializer_class = DepositoSerializer

    def list(self, request, *args, **kwargs):
        queryset = Deposito.objects.filter(carteira__usuario__id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        if request.user.id == instance.carteira.usuario.id or request.user.is_staff == True:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'Erro' : 'Você não está autorizado a ver essa carteira'})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        carteira = Carteira.objects.filter(usuario__id=request.user.id).first()
        self.perform_create(serializer, carteira)
        carteira.valor_disponivel = carteira.valor_disponivel + Decimal(serializer.data['valor'])
        carteira.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, carteira):
        serializer.save(carteira=carteira, endereco_ip=get_client_ip(self.request))
    
class SaqueViewSet(viewsets.ModelViewSet):
    queryset = Saque.objects.all()
    serializer_class = SaqueSerializer

    def list(self, request, *args, **kwargs):
        queryset = Saque.objects.filter(carteira__usuario__id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        if request.user.id == instance.carteira.usuario.id or request.user.is_staff == True:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'Erro' : 'Você não está autorizado a ver essa carteira'})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        carteira = Carteira.objects.filter(usuario__id=request.user.id).first()
        self.perform_create(serializer, carteira)
        carteira.valor_disponivel = carteira.valor_disponivel - Decimal(serializer.data['valor'])
        carteira.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, carteira):
        serializer.save(carteira=carteira, endereco_ip=get_client_ip(self.request))

class AtivoViewSet(viewsets.ModelViewSet):
    queryset = Ativo.objects.all()
    serializer_class = AtivoSerializer

class MovimentacaoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

    def list(self, request, *args, **kwargs):
        queryset = Movimentacao.objects.filter(carteira__usuario__id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ativo = Ativo.objects.filter(id = serializer.data['ativo']).first()
        acao = AcaoMovimentacao.objects.filter(id = serializer.data['acao']).first()
        carteira = Carteira.objects.filter(usuario__id=request.user.id).first()
        if serializer.data['acao'] == 2:
            aplicacao = Aplicacao.objects.filter(movimentacao__ativo=ativo, movimentacao__carteira=carteira, movimentacao__carteira__usuario=request.user, status_aplicacao=True).first()
            if not aplicacao:
                return Response({"Erro": "Não existem aplicações no ativo selecionado"})
        
        if carteira.valor_disponivel < (Decimal(serializer.data['quantidade']) * ativo.valor_unitario):
            return Response({"Erro": "Não existe valor suficiente na carteira para fazer essa aplicação."})
        movimentacao = Movimentacao.objects.create(
            ativo=ativo,
            quantidade=serializer.data['quantidade'],
            preco_unitario=ativo.valor_unitario,
            endereco_ip=get_client_ip(request),
            acao=acao,
            carteira=carteira
        )
        movimentacao.save()
        if serializer.data['acao'] == 1:
            carteira.valor_disponivel = carteira.valor_disponivel - (Decimal(serializer.data['quantidade']) * ativo.valor_unitario)
            carteira.valor_aplicado += (Decimal(serializer.data['quantidade']) * ativo.valor_unitario)
            aplicacao = Aplicacao.objects.create(
                movimentacao=movimentacao,
                status_aplicacao = True
            )
            aplicacao.save()
        if serializer.data['acao'] == 2:
            if Decimal(serializer.data['quantidade']) * ativo.valor_unitario > Decimal(aplicacao.movimentacao.quantidade) * ativo.valor_unitario:
                return Response({"Erro": "Não existe valor suficiente na aplicação para fazer essa retirada."})                
            carteira.valor_disponivel = carteira.valor_disponivel + (Decimal(serializer.data['quantidade']) * ativo.valor_unitario)
            carteira.valor_aplicado -= (Decimal(serializer.data['quantidade']) * ativo.valor_unitario)
            retirada = Retirada.objects.create(
                movimentacao=movimentacao,
                aplicacao=aplicacao
            )
            retirada.save()
            aplicacao.status_aplicacao=False
            aplicacao.save()
        carteira.save()
        headers = self.get_success_headers(serializer.data)


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)