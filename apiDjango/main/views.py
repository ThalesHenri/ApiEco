from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
import mercadopago


sdk = mercadopago.SDK("APP_USR-5237973553263513-092214-250da3bfa9cecb82716a879e4e0087a4-2707980774")  # substitua pelo seu access token
    
class CompradorViewSet(viewsets.ModelViewSet):
    queryset = Comprador.objects.all()
    serializer_class = CompradorSerializer
    
    
class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
    
    
class PacoteViewSet(viewsets.ModelViewSet):
    queryset = Pacote.objects.all()
    serializer_class = PacoteSerializer
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
    
class PacoteViewSet(viewsets.ModelViewSet):
    queryset = Pacote.objects.all()
    serializer_class = PacoteSerializer
    permission_classes = [AllowAny] # por enquanto
    parser_classes = [MultiPartParser, FormParser] # para upload de imagem


    def get_queryset(self):
        
        queryset = super().get_queryset()
        vendedor = self.request.query_params.get('vendedor')
        if vendedor:
            queryset = queryset.filter(vendedor_id=int(vendedor))
        return queryset

    
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]  # ajustar depois

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pedido = serializer.save()

        # Criação da preferência no Mercado Pago
        preference_data = {
            "items": [
                {
                    "id": str(pedido.pacote.id),
                    "title": pedido.pacote.nome_pacote,
                    "quantity": 1,
                    "unit_price": float(pedido.preco_total),
                    "currency_id": "BRL",
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8000/pagamento-sucesso/",
                "failure": "http://127.0.0.1:8000/pagamento-falha/",
                "pending": "http://127.0.0.1:8000/pagamento-pendente/"
            },
            "payer":{
                "name":pedido.comprador.nome,
                "email":pedido.comprador.user.email
            }
            
        }

        result = sdk.preference().create(preference_data)
        print(preference_data["payer"])
        if result["status"] == 201:
            pagamento_info = result["response"]

            # Salvar o ID da preferência no pedido
            pedido.cobranca_id = pagamento_info["id"]
            pedido.init_point = pagamento_info["init_point"]  # preference_id
            pedido.save()

            response_data = serializer.data
            response_data["init_point"] = pagamento_info["init_point"]  # URL checkout
            return Response(response_data, status=201)
        elif result["status"] == 400:
            return Response({"error": "Erro ao criar preferência de pagamento."}, status=400)
        return Response({"error": "Erro ao criar preferência de pagamento."}, status=400)

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    
    
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    
    
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