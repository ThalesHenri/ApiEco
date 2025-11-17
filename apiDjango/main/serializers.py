from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

        
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adiciona informações customizadas ao token
        token['tipo'] = user.tipo
        if hasattr(user, 'vendedor'):
            token['real_id'] = user.vendedor.id
        
        #token['real_ID'] = user.

        return token
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
        fields = '__all__'
        
        
        
class PacoteSerializer(serializers.ModelSerializer):
    nome_vendedor = serializers.CharField(source='vendedor_id.nome_empresa', read_only=True)
    class Meta:
        model = Pacote
        fields = ['id', 'vendedor_id','nome_vendedor', 'nome_pacote', 'preco', 'descricao', 'quant_disponivel', 'categoria', 'imagem']
        extra_kwargs = {
            "imagem": {"required": False, "allow_null": True},
        }
        
        

       
class PedidoSerializer(serializers.ModelSerializer):
    nome_pacote = serializers.CharField(source='pacote.nome_pacote', read_only=True)
    nome_vendedor = serializers.CharField(source='pacote.vendedor_id.nome_empresa', read_only=True)
    nome_comprador = serializers.CharField(source='comprador.nome', read_only=True)
    email_comprador = serializers.EmailField(source='comprador.user.email', read_only=True)
    telefone_comprador = serializers.CharField(source='comprador.telefone', read_only=True)
    data_compra = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True,source='data_pedido')
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
    

class CompradorRegisterSerializer(serializers.ModelSerializer):
    # Campos do User
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Comprador
        fields = ['nome', 'telefone', 'email', 'username', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está cadastrado.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def create(self, validated_data):
        # Extrai os dados do usuário
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # Cria o usuário com tipo 'comprador'
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            tipo='comprador'
        )

        # Cria o comprador vinculado ao usuário
        comprador = Comprador.objects.create(user=user, **validated_data)
        return comprador