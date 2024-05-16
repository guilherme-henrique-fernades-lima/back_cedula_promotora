from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from integration.core.models import PreContrato
from integration.core.serializer import PreContratoMS
import pandas as pd
from datetime import datetime, timedelta


class PreContratosViewSet(viewsets.ModelViewSet):
    queryset = PreContrato.objects.all()
    serializer_class = PreContratoMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):       

        dt_inicio = request.GET.get("dt_inicio", datetime.now() - timedelta(days=1))
        dt_final = request.GET.get("dt_final", datetime.now())

        #TODO listar pelo id_user

        try:           
            pre_contratos = PreContrato.objects.filter(dt_pag_cliente__range=[dt_inicio, dt_final]).order_by('-dt_digitacao')
            serializer = PreContratoMS(pre_contratos, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):

        try:
            pre_contratos = PreContrato.objects.get(nr_PreContrato=pk)
            serializer = PreContratoMS(pre_contratos)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        try:
            serializer = PreContratoMS(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):

        try:
            pre_contratos = PreContrato.objects.get(id=pk)
            serializer = PreContratoMS(instance=pre_contratos, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        id = request.GET.get("id")

        try:
            pre_contratos = PreContrato.objects.get(id=id)
            pre_contratos.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        