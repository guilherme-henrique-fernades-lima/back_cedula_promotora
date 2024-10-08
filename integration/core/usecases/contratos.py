import pandas as pd

class DashboardContratos():

    def empty_object(self):
        return {
            'indicadores': {
                'bancos': [],
                'corretores': [],
                'convenios': [],
                'promotoras': [],
                'operacoes': [],               
                'tt_contratos': 0,
                'tt_vl_contratos': 0,
                'tt_vl_comissoes': 0
            },
            'data': [],
        }

    def execute(self, data): 

        #print(data)      

        '''
            VISÕES OBRIGATÓRIAS:
            - VLR TOTAL CONTRATOS
            - VLR TOAL COMISSÃO 
            - QTD TT CONTRATOS

            FILTROS:
            - POR DATA
            - POR CONVÊNIO
            - POR OPERACAO 
            - POR BANCO API
            - POR PROMOTORA API
            - POR CORRETOR API
        '''

        df = pd.DataFrame.from_dict(data)
        pd.set_option('display.expand_frame_repr', False)    

        if df.empty: 
             return self.empty_object() 

        #Converter as colunas para tipo float
        df["vl_contrato"] = df["vl_contrato"].astype(float)
        df["vl_parcela"] = df["vl_parcela"].astype(float)
        df["vl_comissao"] = df["vl_comissao"].astype(float)

        #Totalizadores gerais
        tt_contratos = df[['nr_contrato']].count()
        tt_vl_contratos = df[['vl_contrato']].sum()
        tt_vl_comissoes = df[['vl_comissao']].sum()
        print(tt_contratos)

        #Totalizadores BANCOS
        bancos = df.groupby(['nome_banco'], as_index=False)['vl_contrato'].agg(['sum','count']).rename(columns={'sum':'vlr_total', 'count': 'qtd'}).sort_values(by=['qtd'], ascending=False).reset_index()
        bancos['perc_qtd'] = round(bancos['qtd']/bancos['qtd'].sum() * 100,2)
        tt_bancos = bancos.to_dict('records')

        #Totalizadores CORRETORES
        corretores = df.groupby(['nome_corretor'], as_index=False)['vl_contrato'].agg(['sum','count']).rename(columns={'sum':'vlr_total', 'count': 'qtd'}).sort_values(by=['qtd'], ascending=False).reset_index()
        corretores['perc_qtd'] = round(corretores['qtd']/corretores['qtd'].sum() * 100,2)
        tt_corretores = corretores.to_dict('records')

        #Totalizadores CONVÊNIOS
        convenios = df.groupby(['nome_convenio'], as_index=False)['vl_contrato'].agg(['sum','count']).rename(columns={'sum':'vlr_total', 'count': 'qtd'}).sort_values(by=['qtd'], ascending=False).reset_index()
        convenios['perc_qtd'] = round(convenios['qtd']/convenios['qtd'].sum() * 100,2)
        tt_convenios = convenios.to_dict('records')

        #Totalizadores PROMOTORAS
        promotoras = df.groupby(['nome_promotora'], as_index=False)['vl_contrato'].agg(['sum','count']).rename(columns={'sum':'vlr_total', 'count': 'qtd'}).sort_values(by=['qtd'], ascending=False).reset_index()
        promotoras['perc_qtd'] = round(promotoras['qtd']/promotoras['qtd'].sum() * 100,2)
        tt_promotoras = promotoras.to_dict('records')

        #Totalizadores OPERAÇÕES
        operacoes = df.groupby(['nome_operacao'], as_index=False)['vl_contrato'].agg(['sum','count']).rename(columns={'sum':'vlr_total', 'count': 'qtd'}).sort_values(by=['qtd'], ascending=False).reset_index()
        operacoes['perc_qtd'] = round(operacoes['qtd']/operacoes['qtd'].sum() * 100,2)
        tt_operacoes = operacoes.to_dict('records')

        #breakpoint()

        return {
            'indicadores': {
                'bancos': tt_bancos,
                'corretores': tt_corretores,
                'convenios': tt_convenios,
                'promotoras': tt_promotoras,
                'operacoes': tt_operacoes,                
                'tt_contratos': tt_contratos,
                'tt_vl_contratos': tt_vl_contratos,
                'tt_vl_comissoes': tt_vl_comissoes
            },
            'data': df.to_dict('records'),
        }

if __name__ == '__main__':
    from integration.core.usecases.contratos import DashboardContratos
    etl = DashboardContratos()    
    #etl.execute(data) #Popular o execute com o data
    etl.execute()
