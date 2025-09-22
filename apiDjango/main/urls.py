from django.urls import path,include
from .views import *  
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('compradores',CompradorViewSet)
router.register('vendedores',VendedorViewSet)
router.register('pacotes',PacoteViewSet)
router.register('pedidos',PedidoViewSet)
router.register('avaliacoes',AvaliacaoViewSet)
router.register('pagamentos',PagamentoViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('token/',CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('testePrivado/', ViewTest.as_view(), name='view-test'),
    path('registerVendedor/', VendedoresRegisterView.as_view(), name='vendedor-register'),
    path('registerComprador/', CompradoresRegisterView.as_view(), name='comprador-register'),
    path('testePublico/', TestePublico.as_view(), name='teste-publico'),   
]