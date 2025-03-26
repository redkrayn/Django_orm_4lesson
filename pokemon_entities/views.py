import django
import folium

from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        if pokemon_entity.disappeared_at > django.utils.timezone.localtime() > pokemon_entity.appeared_at:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url) if pokemon_entity.pokemon.photo else None
            )

    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=int(pokemon_id))

    if pokemon.previous_evolution:
        back_evolution = Pokemon.objects.get(title=pokemon.previous_evolution)
        previous_evolution = {
            'pokemon_id': back_evolution.id,
            'img_url': request.build_absolute_uri(back_evolution.photo.url) if back_evolution.photo else None,
            'title_ru': back_evolution.title,
        }
    else:
        previous_evolution = None

    next_evolution = pokemon.back.all()

    if next_evolution.exists():
        for pokemon_evolution in next_evolution:
            evolutions_list = {
                'pokemon_id': pokemon_evolution.id,
                'img_url': request.build_absolute_uri(pokemon_evolution.photo.url) if pokemon_evolution.photo else None,
                'title_ru': pokemon_evolution.title
            }
    else:
        evolutions_list = None

    pokemons_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': evolutions_list
    }

    try:
        requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in requested_pokemon.entities.all():
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url) if pokemon_entity.pokemon.photo else None
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })

