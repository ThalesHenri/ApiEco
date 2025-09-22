from django.contrib import admin
from .models import *

# Register your models here.



admin.site.register(Comprador)
admin.site.register(Vendedor)
admin.site.register(Pacote)
admin.site.register(Pedido)
admin.site.register(Avaliacao)
admin.site.register(Pagamento)