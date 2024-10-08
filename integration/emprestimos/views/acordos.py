from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated
from integration.emprestimos.models import Acordo, Emprestimo, EmprestimoParcela, AcordoParcela
from integration.emprestimos.serializer import AcordoMS
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from integration.emprestimos.repository.acordos import AcordosRepository
from integration.emprestimos.usecases.etl.acordos import EtlAcordos


class AcordosViewSet(viewsets.ModelViewSet):
    queryset = Acordo.objects.all()
    serializer_class = AcordoMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer  
    
            
    def list(self, request):    
        print('Entrou no list de acordos...')

        try:
            dt_inicio = request.GET.get("dt_inicio", datetime.now() - timedelta(days=1))
            dt_final = request.GET.get("dt_final", datetime.now())
            dt_filter = request.GET.get("dt_filter","")         

            acordo_repository = AcordosRepository()
            acordos = acordo_repository.get_acordos(dt_inicio, dt_final, dt_filter)

            etl = EtlAcordos()
            data_etl = etl.execute(acordos)           

            return Response(data=data_etl, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)     

    def create(self, request):   
        print('Entrou aqui')
      
        try:
            id_emprestimo = request.GET.get("id_emprestimo")
            data = request.data
            print(request.data)

            with transaction.atomic(): 
                if id_emprestimo:
                    emprestimo = Emprestimo.objects.get(id=id_emprestimo)
                    emprestimo.status = 'acordo'
                    emprestimo.save()       

                    parcelas = EmprestimoParcela.objects.filter(
                        emprestimo=id_emprestimo
                    ).exclude( 
                        status_pagamento__in=['pago', 'pago_parcial']
                    ) 

                    for parcela in parcelas:
                        parcela.tp_pagamento = 'acordo'
                        parcela.save()

       
                serializer = AcordoMS(data=data) 
                if serializer.is_valid():
                    acordo = serializer.save()

                    data_emprestimo = datetime.strptime(data['dt_cobranca'], "%Y-%m-%d")
                    vl_parcela = data['vl_parcela']
                    installments = []

                    for parcela in range(data['qt_parcela']):
                            mes_cobranca = parcela + 0
                            nr_parcela = parcela + 1
                            due_date = (data_emprestimo + relativedelta(months=mes_cobranca)).date()

                            installment = AcordoParcela(
                                dt_vencimento=due_date,
                                nr_parcela=nr_parcela,
                                dt_pagamento=None,
                                tp_pagamento="parcela",
                                status_pagamento="pendente",
                                vl_parcial=None,
                                vl_parcela= vl_parcela,
                                acordo=acordo,
                                qtd_tt_parcelas=data['qt_parcela']
                            )

                            installments.append(installment)                    

                    AcordoParcela.objects.bulk_create(installments)
                    
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
               
    def retrieve(self, request, pk):     

        try:
            acordo = AcordosRepository().get_acordo_by_id(pk)

            return Response(data=acordo, status=status.HTTP_200_OK)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):

        try:
            acordo = Acordo.objects.get(id=pk)
            acordo.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            print("Error: ", error)
            return Response(data={'success': False, 'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)