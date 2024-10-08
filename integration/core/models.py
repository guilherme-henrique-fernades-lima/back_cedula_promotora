from django.db import models

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    nome = models.CharField(max_length=150, null=True, blank=True)
    dt_nascimento = models.DateField(null=True, blank=True)
    especie = models.CharField(max_length=100, null=True, blank=True)
    matricula = models.CharField(max_length=20, null=True, blank=True)
    telefone1 = models.CharField(max_length=20, null=True, blank=True)
    telefone2 = models.CharField(max_length=20, null=True, blank=True)   
    observacoes = models.TextField(null=True, blank=True)
    convenio = models.CharField(max_length=100, null=True, blank=True)
    senha = models.CharField(max_length=60, null=True, blank=True)
    created_by_user_id = models.IntegerField(null=True, blank=True)
    canal_aquisicao = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'core_cliente'

class Contrato(models.Model):
    id = models.BigAutoField(primary_key=True)
    promotora = models.CharField(max_length=255, null=True, blank=True)
    dt_digitacao = models.DateField(null=True, blank=True)
    nr_contrato = models.CharField(max_length=255, null=True, blank=True)
    no_cliente = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=255, null=True, blank=True)
    convenio = models.CharField(max_length=255, null=True, blank=True)
    operacao = models.CharField(max_length=255, null=True, blank=True)
    banco = models.CharField(max_length=255, null=True, blank=True)
    vl_contrato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qt_parcelas = models.CharField(max_length=255, null=True, blank=True)
    vl_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dt_pag_cliente = models.DateField(null=True, blank=True)
    dt_pag_comissao = models.CharField(max_length=255, null=True, blank=True)
    vl_comissao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    porcentagem = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corretor = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tabela = models.CharField(max_length=60, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=20, null=True, blank=True) 
    status_comissao = models.CharField(max_length=30, null=True, blank=True)    
    iletrado = models.BooleanField(blank=True, null=True)
    documento_salvo = models.BooleanField(blank=True, null=True) 
    representante_legal = models.BooleanField(blank=True, null=True)
    id_pre_contrato = models.IntegerField(null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'core_contrato'
        
class Despesa(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_vencimento = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    situacao = models.CharField(max_length=100, null=True, blank=True)
    tp_despesa = models.CharField(max_length=100, null=True, blank=True)
    natureza_despesa = models.CharField(max_length=100, null=True, blank=True)
    id_loja = models.IntegerField(null=True, blank=True)

class Emprestimo(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_emprestimo = models.DateField(blank=True, null=True)
    no_cliente = models.CharField(max_length=255, blank=True)
    vl_emprestimo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vl_capital = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vl_juros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vl_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qt_parcela = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    observacao = models.TextField(blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True)
    logradouro = models.CharField(max_length=255, null=True)
    numLogr = models.CharField(max_length=255, null=True)
    complLogr = models.CharField(max_length=255, null=True)
    bairro = models.CharField(max_length=255, null=True)
    cidade = models.CharField(max_length=255, null=True)
    estado = models.CharField(max_length=10, null=True)

class EmprestimoItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt_vencimento = models.DateField(blank=True, null=True)
    nr_parcela = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    dt_pagamento = models.DateField(blank=True, null=True)
    tp_pagamento = models.CharField(max_length=100, null=True, blank=True)
    emprestimo = models.ForeignKey(Emprestimo, verbose_name='Emprestimo', related_name='EmprestimoItem', on_delete=models.CASCADE, help_text='Emprestimo')

class Lojas(models.Model):
    id = models.BigAutoField(primary_key=True) 
    is_active = models.BooleanField(default=True, blank=True, null=True)
    sg_loja = models.CharField(max_length=30, blank=True, null=True)
    
class Promotora(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promotoras'

class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'convenios'

class Operacao(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operacoes'

class Banco(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bancos'

class Corretor(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corretores'

class NaturezaDespesa(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'natureza_despesas'

class CanalAquisicaoCliente(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'canal_aquisicao_clientes'

class PreContrato(models.Model):
    id = models.BigAutoField(primary_key=True)    
    promotora = models.CharField(max_length=255, null=True, blank=True)
    dt_digitacao = models.DateField(null=True, blank=True)
    nr_contrato = models.CharField(max_length=60, null=True, blank=True)
    no_cliente = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)
    convenio = models.CharField(max_length=100, null=True, blank=True)
    operacao = models.CharField(max_length=100, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)    
    vl_contrato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    
    qt_parcelas = models.IntegerField(null=True, blank=True) 
    vl_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dt_pag_cliente = models.DateField(null=True, blank=True)
    porcentagem = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corretor = models.CharField(max_length=100, null=True, blank=True)
    tabela = models.CharField(max_length=60, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=20, null=True, blank=True) 
    status_comissao = models.CharField(max_length=30, null=True, blank=True)  
    iletrado = models.BooleanField(blank=True, null=True) 
    documento_salvo = models.BooleanField(blank=True, null=True) 
    user_id_created = models.IntegerField(null=True, blank=True)     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contrato_criado = models.BooleanField(blank=True, null=True, default=False)
    dt_pag_comissao = models.CharField(max_length=255, null=True, blank=True)
    vl_comissao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    representante_legal = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_contratos'

class FuturoContrato(models.Model):
    id = models.BigAutoField(primary_key=True)    
    nome_cliente = models.CharField(max_length=255, null=True, blank=True)
    cpf_cliente = models.CharField(max_length=20, null=True, blank=True)
    nome_rep_legal = models.CharField(max_length=255, null=True, blank=True)
    cpf_rep_legal = models.CharField(max_length=20, null=True, blank=True)
    convenio = models.CharField(max_length=100, null=True, blank=True)
    operacao = models.CharField(max_length=100, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)    
    vl_contrato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    
    observacoes = models.TextField(null=True, blank=True)
    dt_concessao_beneficio = models.DateField(null=True, blank=True)
    dt_efetivacao_emprestimo = models.DateField(null=True, blank=True)
    representante_legal = models.BooleanField(blank=True, null=True)
    iletrado = models.BooleanField(blank=True, null=True)
    tipo_contrato = models.CharField(max_length=20, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'futuros_contratos'



   
