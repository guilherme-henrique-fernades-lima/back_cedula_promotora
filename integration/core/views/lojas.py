from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import  IsAuthenticated
from integration.core.models import Lojas 
from integration.core.serializer import LojasMS

class LojasViewSet(viewsets.ModelViewSet):
    queryset = Lojas.objects.all()
    serializer_class = LojasMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):        

        try:
            only_actives = request.GET.get("ativas", "")

            if only_actives:
                lojas = Lojas.objects.filter(is_active=True)
                serializer = LojasMS(lojas, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
           
            lojas = Lojas.objects.all()           
            serializer = LojasMS(lojas, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

            

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        try:

            data = request.data           
            loja_exists = Lojas.objects.filter(sg_loja=data["sg_loja"])           

            if loja_exists:               
                return Response(data={"message": "Loja já existe"}, status=status.HTTP_403_FORBIDDEN)

            serializer = LojasMS(data=data)           

            if serializer.is_valid():                
                serializer.save()                
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):

        try:
            lojas = Lojas.objects.get(id=pk)
            serializer = LojasMS(lojas)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):

        try:            
            data = request.data              
            lojas = Lojas.objects.get(id=pk)
            serializer = LojasMS(instance=lojas, data=data)

            if serializer.is_valid():
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        try:
            lojas = Lojas.objects.get(id=pk)
            lojas.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
