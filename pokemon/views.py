
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pokemon, Gimnasio, Entrenador


# ==============================
# PAGINA PRINCIPAL - POKEMON
# ==============================

def inicio(request):
    pokemones = Pokemon.objects.all()

    return render(request, 'pokemon/lista.html', {
        'pokemones': pokemones
    })


# ==============================
# LISTA DE POKEMON
# ==============================

def lista_pokemones(request):
    pokemones = Pokemon.objects.all()

    return render(request, 'pokemon/lista.html', {
        'pokemones': pokemones
    })


# ==============================
# LISTA DE GIMNASIOS
# ==============================

def lista_gimnasios(request):
    gimnasios = Gimnasio.objects.all()

    return render(request, 'pokemon/gimnasios.html', {
        'gimnasios': gimnasios
    })


# ==============================
# LISTA DE ENTRENADORES
# ==============================

def lista_entrenadores(request):
    entrenadores = Entrenador.objects.all()

    return render(request, 'pokemon/entrenadores.html', {
        'entrenadores': entrenadores
    })


# ==============================
# EDITAR POKEMON
# ==============================

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


# ==============================
# ELIMINAR POKEMON
# ==============================

def eliminar_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)

    if request.method == 'POST':
        pokemon.delete()
        return redirect('inicio')

    return render(request, 'pokemon/eliminar.html', {
        'pokemon': pokemon
    })
