from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

        
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tipo']


class CompradorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # mostra os dados do user associado

    class Meta:
        model = Comprador
        fields = ['id', 'telefone', 'user']


class VendedorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # mostra os dados do user associado

    class Meta:
        model = Vendedor
        fields = ['id', 'nome_empresa', 'telefone', 'cnpj', 'user','representante']
        
        
        
class PacoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacote
        fields = '__all__'
        
        
        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
        

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
        
class VendedorRegisterSerializer(serializers.ModelSerializer):
    # Campos do User
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Vendedor
        fields = [
            'nome_empresa', 'representante', 'telefone', 'cnpj',
            'email', 'username', 'password'
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está cadastrado.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate_cnpj(self, value):
        if Vendedor.objects.filter(cnpj=value).exists():
            raise serializers.ValidationError("Este CNPJ já está cadastrado.")
        return value

    def create(self, validated_data):
        # Extrai os dados do usuário
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # Cria o usuário com tipo 'vendedor'
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            tipo='vendedor'
        )

        # Cria o vendedor vinculado ao usuário
        vendedor = Vendedor.objects.create(user=user, **validated_data)
        return vendedor