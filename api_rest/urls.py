from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('carteiras', CarteiraViewSet)
router.register('usuarios', UserViewSet)
router.register('deposito', DepositoViewSet)
router.register('saque', SaqueViewSet)
router.register('movimentacao', MovimentacaoViewSet)
router.register('ativos', AtivoViewSet)

urlpatterns = [
]