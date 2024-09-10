from django.urls import path
from inicio.views import index, consultar_cliente, esquecer_cliente

urlpatterns = [
    path('', index),
    path('consultar_cliente/', consultar_cliente, name='consultar_cliente'),
    path('esquecer_cliente/', esquecer_cliente, name='esquecer_cliente')
]