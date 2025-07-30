from django.urls import path,include
from .views import *  
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('compradores',CompradorViewSet)
router.register('vendedores',VendedorViewSet)
router.register('pacotes',PacoteViewSet)
router.register('pedidos',PedidoViewSet)
router.register('avaliacoes',AvaliacaoViewSet)
router.register('pagamentos',PagamentoViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('testePrivado/', ViewTest.as_view(), name='view-test'),
    path('registerVendedores/', VendedoresRegisterView.as_view(), name='vendedor-register'),
    path('testePublico/', TestePublico.as_view(), name='teste-publico'),   
]