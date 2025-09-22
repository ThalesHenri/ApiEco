from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView


    
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
    def get_queryset(self):
        
        queryset = super().get_queryset()
        vendedor = self.request.query_params.get('vendedor')
        print(vendedor)
        if vendedor:
            queryset = queryset.filter(vendedor_id=int(vendedor))
            print(queryset)
        return queryset

    
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [AllowAny] # por enquanto
    

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