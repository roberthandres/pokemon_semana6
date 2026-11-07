
import requests

from django.shortcuts import render, get_object_or_404, redirect
from .models import Pokemon, Gimnasio, Entrenador


# =====================================
# PAGINA PRINCIPAL
# =====================================

def inicio(request):
    pokemones = Pokemon.objects.all()

    return render(request, 'pokemon/lista.html', {
        'pokemones': pokemones
    })


# =====================================
# LISTA DE POKEMON
# =====================================

def lista_pokemones(request):
    pokemones = Pokemon.objects.all()

    return render(request, 'pokemon/lista.html', {
        'pokemones': pokemones
    })


# =====================================
# LISTA DE GIMNASIOS
# =====================================

def lista_gimnasios(request):
    gimnasios = Gimnasio.objects.all()

    return render(request, 'pokemon/gimnasios.html', {
        'gimnasios': gimnasios
    })


# =====================================
# LISTA DE ENTRENADORES
# =====================================

def lista_entrenadores(request):
    entrenadores = Entrenador.objects.all()

    return render(request, 'pokemon/entrenadores.html', {
        'entrenadores': entrenadores
    })


# =====================================
# EDITAR POKEMON
# =====================================

def editar_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

    if request.method == 'POST':
        pokemon.nombre = request.POST.get('nombre')
        pokemon.peso = request.POST.get('peso')
        pokemon.naturaleza = request.POST.get('naturaleza')
        pokemon.elemento = request.POST.get('elemento')
        pokemon.habilidades = request.POST.get('habilidades')
        pokemon.descripcion = request.POST.get('descripcion')
        pokemon.imagen = request.POST.get('imagen') or None

        pokemon.save()

        return redirect('inicio')

    return render(request, 'pokemon/editar.html', {
        'pokemon': pokemon
    })


# =====================================
# ELIMINAR POKEMON
# =====================================

def eliminar_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

    if request.method == 'POST':
        pokemon.delete()
        return redirect('inicio')

    return render(request, 'pokemon/eliminar.html', {
        'pokemon': pokemon
    })


# =====================================
# CONSULTAR POKEMON EN POKEAPI
# =====================================

def consultar_api(request):
    nombre = request.GET.get('nombre', '').strip().lower()

    pokemon_api = None
    error = None

    if nombre:
        url = f'https://pokeapi.co/api/v2/pokemon/{nombre}'

        try:
            # Consultar la API
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()

            datos = respuesta.json()

            # Buscar si el Pokémon ya está guardado
            pokemon_guardado = Pokemon.objects.filter(
                nombre__iexact=datos['name']
            ).first()

            # Obtener las imágenes
            sprites = datos.get('sprites', {})

            imagen = (
                sprites.get('other', {})
                .get('official-artwork', {})
                .get('front_default')
            )

            if not imagen:
                imagen = sprites.get('front_default')

            # Organizar los datos del Pokémon
            pokemon_api = {
                'id': pokemon_guardado.id if pokemon_guardado else None,
                'nombre': datos['name'].capitalize(),
                'imagen': imagen,
                'peso': datos['weight'] / 10,
                'altura': datos['height'] / 10,

                'elementos': [
                    tipo['type']['name'].capitalize()
                    for tipo in datos['types']
                ],

                'habilidades': [
                    habilidad['ability']['name'].capitalize()
                    for habilidad in datos['abilities']
                ]
            }

        except requests.exceptions.HTTPError:
            error = 'No se encontró ese Pokémon. Intenta con otro nombre.'

        except requests.exceptions.RequestException:
            error = 'No fue posible conectar con PokéAPI.'

        except (KeyError, TypeError, ValueError):
            error = 'No se pudo interpretar la información del Pokémon.'

    return render(request, 'pokemon/consultar_api.html', {
        'pokemon': pokemon_api,
        'error': error,
        'nombre': nombre
    })

# =====================================
# JUEGO: ADIVINA EL POKEMON
# =====================================

def juego_pokemon(request):
    pokemon = None
    mensaje = ''
    terminado = False

    if request.method == 'POST':
        nombre_correcto = request.POST.get('nombre_correcto', '').lower()
        respuesta = request.POST.get('respuesta', '').strip().lower()

        if respuesta == nombre_correcto:
            mensaje = '¡Correcto! ¡Adivinaste el Pokémon!'
        else:
            mensaje = f'¡Incorrecto! El Pokémon era {nombre_correcto.capitalize()}.'

        terminado = True

        pokemon = {
            'nombre': nombre_correcto.capitalize(),
            'imagen': request.POST.get('imagen', '')
        }

    else:
        import random

        numero = random.randint(1, 151)
        url = f'https://pokeapi.co/api/v2/pokemon/{numero}'

        try:
            respuesta_api = requests.get(url, timeout=10)
            respuesta_api.raise_for_status()
            datos = respuesta_api.json()

            pokemon = {
                'nombre': datos['name'].capitalize(),
                'imagen': datos['sprites']['other']['official-artwork']['front_default']
            }

        except requests.exceptions.RequestException:
            mensaje = 'No se pudo conectar con PokéAPI. Intenta nuevamente.'

    return render(request, 'pokemon/juego.html', {
        'pokemon': pokemon,
        'mensaje': mensaje,
        'terminado': terminado
    })

