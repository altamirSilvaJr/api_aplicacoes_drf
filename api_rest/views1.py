from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from . serializers import *

class ModalidadeApiView(APIView):
    def get(self, request):
        modalidades = Modalidade.objects.all()
        serializer = ModalidadeSerializer(modalidades, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = ModalidadeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
