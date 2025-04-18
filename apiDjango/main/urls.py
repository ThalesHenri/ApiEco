from django.urls import path,include
from .views import (UsuarioViewSet,CompradorViewSet,VendedorViewSet,PacoteViewSet,PedidoViewSet,AvaliacaoViewSet,PagamentoViewSet)  
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('usuarios',UsuarioViewSet)
router.register('compradores',CompradorViewSet)
router.register('vendedores',VendedorViewSet)
router.register('pacotes',PacoteViewSet)
router.register('pedidos',PedidoViewSet)
router.register('avaliacoes',AvaliacaoViewSet)
router.register('pagamentos',PagamentoViewSet)


urlpatterns = [
    path('',include(router.urls))
]