from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    ]
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return self.nome

class Comprador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    email = models.EmailField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} (Comprador)"

class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=100)
    frete = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.EmailField()
    cnpj = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_empresa

class Pacote(models.Model):
    CATEGORIA_CHOICES = [
        ('Salgada', 'Salgada'),
        ('Mista', 'Mista'),
        ('Doce', 'Doce'),
    ]
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    nome_pacote = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField()
    quant_disponivel = models.IntegerField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return self.nome_pacote

class Pedido(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE)
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    status_pagamento = models.CharField(max_length=50)
    preco_total = models.DecimalField(max_digits=8, decimal_places=2)
    status_pedido = models.CharField(max_length=50)
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk}"

class Pagamento(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    status_pagamento = models.CharField(max_length=50)
    data_compra = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=50)

    def __str__(self):
        return f"Pagamento #{self.pk} - Pedido #{self.pedido.pk}"

class Avaliacao(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    avaliacao = models.PositiveSmallIntegerField()  # 1 a 10
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.vendedor} por {self.comprador}"
