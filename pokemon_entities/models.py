import datetime
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название на японском')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', related_name='back',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Из кого эволюционировал'
    )
    photo = models.ImageField(null=True, blank=True, verbose_name='Картинка', upload_to='media/')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entities', on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта', null=True, blank=True)
    lon = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    appeared_at = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Дата появления покемона',
        null=True,
        blank=True
    )
    disappeared_at = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=7),
        verbose_name='Дата исчезновения покемона',
        null=True,
        blank=True
    )
    level = models.PositiveSmallIntegerField(default=20, verbose_name='Уровень', null=True, blank=True)
    health = models.PositiveSmallIntegerField(default=20, verbose_name='Здоровье', null=True, blank=True)
    damage = models.PositiveSmallIntegerField(default=20, verbose_name='Урон', null=True, blank=True)
    defence = models.PositiveSmallIntegerField(default=20, verbose_name='Защита', null=True, blank=True)
    endurance = models.PositiveSmallIntegerField(default=20, verbose_name='Выносливость', null=True, blank=True)

