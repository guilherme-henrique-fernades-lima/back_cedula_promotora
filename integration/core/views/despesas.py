from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from integration.core.models import Despesa 
from integration.core.serializer import DespesaMS
from integration.core.models import Contrato 
from integration.core.serializer import ContratoMS
import pandas as pd
from datetime import datetime, timedelta
from integration.core.usecases.despesas import DashboardDespesas
from integration.core.repository.despesas import DespesasRepository


class DespesasViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.all()
    serializer_class = DespesaMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):

        try:

            dt_inicio = request.GET.get("dt_inicio", datetime.now() - timedelta(days=1))
            dt_final = request.GET.get("dt_final", datetime.now())

            depesas_repository = DespesasRepository()
            despesas = depesas_repository.get_despesas(dt_inicio, dt_final)

            contratos = depesas_repository.get_comissoes(dt_inicio, dt_final)        

            df = pd.DataFrame.from_dict(despesas)
            df_contratos = pd.DataFrame.from_dict(contratos)
            pd.set_option('display.expand_frame_repr', False)   

            if df_contratos.empty:
                df_contratos = pd.DataFrame({'id': [], 'vl_comissao': []})

            if df.empty:
                df = pd.DataFrame({'id': [], 'dt_vencimento': [], 'descricao': [], 'valor': [], 'situacao': [], 'tp_despesa': [], 'natureza_despesa': [], 'id_loja': []})
          
            if df.empty and df_contratos.empty:
                data = {
                    'data': [],
                    'indicadores': {
                        "pago": 0, 
                        "pendente": 0, 
                        "total": 0,
                        'qtd_tt_comissao': 0,
                        'vl_tt_comissao': 0
                    }
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            if not df_contratos.empty:
                df_contratos["vl_comissao"] = df_contratos["vl_comissao"].astype(float)

            if not df.empty:
                df["valor"] = df["valor"].astype(float)

            soma_por_situacao = df.groupby("situacao")["valor"].sum().reset_index()
            soma_por_situacao_dict = dict(zip(soma_por_situacao["situacao"], soma_por_situacao["valor"]))
           
            data = {
                'data': despesas,
                'indicadores': {
                    "pago": soma_por_situacao_dict.get("pago", 0), 
                    "pendente": soma_por_situacao_dict.get("pendente", 0), 
                    "total": df["valor"].sum(),
                    'qtd_tt_comissao': df_contratos["id"].count(),
                    'vl_tt_comissao': df_contratos["vl_comissao"].sum()
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):

        try:
            despesas = Despesa.objects.get(id=pk)
            serializer = DespesaMS(despesas)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        try:
            serializer = DespesaMS(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):

        try:
            despesa = Despesa.objects.get(id=pk)
            serializer = DespesaMS(instance=despesa, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        try:
            despesa = Despesa.objects.get(id=pk)
            despesa.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='dashboard')
    def dashboard_despesas(self, request):  
        # Endereço API: http://127.0.0.1:8005/integration/despesas/dashboard/

        dt_inicio = request.GET.get("dt_inicio", datetime.now() - timedelta(days=1))
        dt_final = request.GET.get("dt_final", datetime.now())
        loja = request.GET.get("loja", "")    

        try:

            if loja: 
                 if Despesa.objects.filter(id_loja=int(loja)).exists():                            
                    despesas = Despesa.objects.filter(dt_vencimento__range=[dt_inicio, dt_final], id_loja=int(loja)).order_by('dt_vencimento')
                 else:
                    despesas = Despesa.objects.none()
              
                 serializer_despesas = DespesaMS(despesas, many=True)
                 
                 contratos = Contrato.objects.filter(dt_pag_cliente__range=[dt_inicio, dt_final]).order_by('dt_pag_cliente')
                 serializer_contratos = ContratoMS(contratos, many=True)                 
                 
                 etl = DashboardDespesas()
                 data = etl.execute(serializer_despesas.data, serializer_contratos.data, dt_inicio, dt_final)

                 return Response(data=data, status=status.HTTP_200_OK)
            
            else:    

                despesas = Despesa.objects.filter(dt_vencimento__range=[dt_inicio, dt_final]).order_by('dt_vencimento')
                serializer_despesas = DespesaMS(despesas, many=True)

                contratos = Contrato.objects.filter(dt_pag_cliente__range=[dt_inicio, dt_final]).order_by('dt_pag_cliente')
                serializer_contratos = ContratoMS(contratos, many=True)
            
                etl = DashboardDespesas()
                data = etl.execute(serializer_despesas.data, serializer_contratos.data, dt_inicio, dt_final)
                return Response(data=data, status=status.HTTP_200_OK)

            
        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)