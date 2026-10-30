
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Pokemon, Entrenador, Gimnasio


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'peso',
        'naturaleza',
        'elemento',
        'botones',
    )

    def botones(self, obj):
        editar_url = reverse(
            'admin:pokemon_pokemon_change',
            args=[obj.pk]
        )

        eliminar_url = reverse(
            'admin:pokemon_pokemon_delete',
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}" style="background-color:#3498db;'
            'color:white;padding:6px 12px;border-radius:5px;'
            'text-decoration:none;margin-right:8px;">Editar</a>'
            '<a href="{}" style="background-color:#e74c3c;'
            'color:white;padding:6px 12px;border-radius:5px;'
            'text-decoration:none;">Eliminar</a>',
            editar_url,
            eliminar_url
        )

    botones.short_description = 'Acciones'


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'nombre', 'apellido')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('id_documento',)
        return ()


@admin.register(Gimnasio)
class GimnasioAdmin(admin.ModelAdmin):
    list_display = ('lider_del_gym', 'naturaleza', 'elemento')
