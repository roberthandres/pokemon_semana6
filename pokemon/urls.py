
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('pokemones/', views.lista_pokemones, name='lista_pokemones'),

    path('gimnasios/', views.lista_gimnasios, name='lista_gimnasios'),

    path('entrenadores/', views.lista_entrenadores, name='lista_entrenadores'),

    path('editar/<int:id>/', views.editar_pokemon, name='editar_pokemon'),

    path('eliminar/<int:id>/', views.eliminar_pokemon, name='eliminar_pokemon'),

    path('consultar-api/', views.consultar_api, name='consultar_api'),

    path('juego/', views.juego_pokemon, name='juego_pokemon'),
]
