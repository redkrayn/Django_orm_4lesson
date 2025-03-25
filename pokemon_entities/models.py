import datetime
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название на японском')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', related_name='back_evolution',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Из кого эволюционировал'
    )
    photo = models.ImageField(null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entities', on_delete=models.CASCADE, verbose_name='Покемон')
    Lat = models.FloatField(verbose_name='Широта')
    Lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Начало')
    disappeared_at = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=7),
        verbose_name='Конец'
    )
    Level = models.IntegerField(default=20, verbose_name='Уровень')
    Health = models.IntegerField(default=20, verbose_name='Здоровье')
    Damage = models.IntegerField(default=20, verbose_name='Урон')
    Defence = models.IntegerField(default=20, verbose_name='Защита')
    Endurance = models.IntegerField(default=20, verbose_name='Выносливость')

