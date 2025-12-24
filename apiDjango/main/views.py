from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
import mercadopago


sdk = mercadopago.SDK("APP_USR-5237973553263513-092214-250da3bfa9cecb82716a879e4e0087a4-2707980774")  # substitua pelo seu access token
    
class CompradorViewSet(viewsets.ModelViewSet):
    queryset = Comprador.objects.all()
    serializer_class = CompradorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Comprador.objects.filter(user=self.request.user)
    
    
class VendedorViewSet(viewsets.ModelViewSet):   
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vendedor.objects.filter(user=self.request.user)
    
    
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
    
class PacoteViewSet(viewsets.ModelViewSet):
    queryset = Pacote.objects.all()
    serializer_class = PacoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser] # para upload de imagem


    def get_queryset(self):
        queryset = Pacote.objects.all()
        vendedor = self.request.query_params.get('vendedor')
        if vendedor:
            queryset = queryset.filter(vendedor_id=int(vendedor))
        return queryset

    
from rest_framework.exceptions import PermissionDenied, ValidationError

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()  # ← OBRIGATÓRIO PARA O ROUTER
    serializer_class = PedidoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna APENAS pedidos do usuário logado
        return self.queryset.filter(
            comprador__user=self.request.user
        )

    def perform_create(self, serializer):
        try:
            comprador = Comprador.objects.get(user=self.request.user)
        except Comprador.DoesNotExist:
            raise PermissionDenied("Usuário não é um comprador")

        pedido = serializer.save(comprador=comprador)

        preference_data = {
            "items": [
                {
                    "id": str(pedido.pacote.id),
                    "title": pedido.pacote.nome_pacote,
                    "quantity": pedido.quantidade,
                    "unit_price": float(pedido.preco_total),
                    "currency_id": "BRL",
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8000/pagamento-sucesso/",
                "failure": "http://127.0.0.1:8000/pagamento-falha/",
                "pending": "http://127.0.0.1:8000/pagamento-pendente/"
            },
            "payer": {
                "name": pedido.comprador.nome,
                "email": pedido.comprador.user.email
            }
        }

        result = sdk.preference().create(preference_data)

        if result["status"] != 201:
            raise ValidationError({"pagamento": "Erro ao criar preferência no Mercado Pago"})

        pagamento_info = result["response"]

        pedido.cobranca_id = pagamento_info["id"]
        pedido.init_point = pagamento_info["init_point"]
        pedido.preco_total = (
            pagamento_info["items"][0]["unit_price"] *
            pagamento_info["items"][0]["quantity"]
        )
        pedido.save()

        
class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Pagamento.objects.filter(pedido__comprador__user=self.request.user)


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Avaliacao.objects.filter(pedido__comprador__user=self.request.user)
    
    
#teste de classe protegida
class ViewTest(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    #para cada classe autenticar tem que usar esses dois parametros
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    

#registro de Vendedor

class VendedoresRegisterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "Use POST to register a new vendor."})
    def post(self,request):
        serializer = VendedorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    

class CompradoresRegisterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "Use POST to register a new buyer."})
    def post(self,request):
        serializer = CompradorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class TestePublico(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"msg": "acesso público OK"})
    

class PedidosVendedores(APIView):
    permission_classes = [AllowAny]  # ajustar depois
    def get(self, request, vendedor_id):
        pedidos = Pedido.objects.filter(pacote__vendedor_id=vendedor_id)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)