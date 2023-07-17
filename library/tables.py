import django_tables2 as tables
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.html import format_html

from library import models


class APIGameAvatarColumn(tables.Column):
    def render(self, value):
        if not value:
            placeholder = static('game/avatar/placeholder.png')
            return format_html('<img class="border border-secondary rounded" src="{placeholder}" height="40px", width="40px">', placeholder=placeholder)
        return format_html('<img class="border border-secondary rounded" src="{url}" height="40px", width="40px">', url=value)


class GameAvatarColumn(tables.Column):
    def render(self, value):
        if not value:
            placeholder = static('game/avatar/placeholder.png')
            return format_html('<img class="border border-secondary rounded" src="{placeholder}" height="40px", width="40px">', placeholder=placeholder)
        avatar = static(str(value)[15:])
        return format_html('<img class="border border-secondary rounded" src="{url}" height="40px", width="40px">', url=avatar)


class GenreColumn(tables.Column):
    def render(self, value):
        if not value:
            return format_html('No Genre Added')
        genre = ''.join([genre.name for genre in value.all()])
        return format_html('{value}', value=str(genre))


class PriceColumn(tables.Column):
    def render(self, value):
        if not value:
            return format_html('No Price')
        return format_html('${value}', value=value)


class SteamIdColumn(tables.Column):
    def render(self, value):
        if value:
            url = reverse('game-api-read-detail', kwargs={'steamid': value})
            return format_html('<a class="link-light link-underline-opacity-0 stretched-link" href="{url}">{value}</a>', url=url, value=value)


class TitleColumn(tables.Column):
    def render(self, value):
        if value:
            game = models.Game.objects.get(title=value).id
            url = reverse('game-read-detail', kwargs={'pk': game})
            return format_html('<a class="link-light link-underline-opacity-0 stretched-link" href="{url}">{value}</a>', url=url, value=value)



class APIGamesTable(tables.Table):
    avatar = APIGameAvatarColumn(verbose_name='', empty_values=())
    title = tables.Column(verbose_name='Title', attrs={'td': {'style': 'vertical-align: middle'}})
    steamid = SteamIdColumn(verbose_name='SteamID', attrs={'td': {'style': 'vertical-align: middle'}})
    genre = tables.Column(verbose_name='Genre', attrs={'td': {'style': 'vertical-align: middle'}})
    price = PriceColumn(verbose_name='Price', attrs={'td': {'style': 'vertical-align: middle'}})
    release = tables.Column(verbose_name='Release', attrs={'td': {'style': 'vertical-align: middle'}})

    class Meta:
        model = models.GameFromAPI
        attrs = {'class': 'table table-dark table-hover'}
        row_attrs = {'style': 'transform: rotate(0);'}
        fields = ('steamid', 'avatar', 'title', 'genre', 'price', 'release')
        exclude = ('avatar',)


class GamesTable(tables.Table):
    avatar = GameAvatarColumn(verbose_name='', empty_values=(), attrs={'td': {'class': 'd-flex justify-content-center'}})
    title = TitleColumn(verbose_name='Title', attrs={'td': {'style': 'vertical-align: middle'}})
    genre = GenreColumn(verbose_name='Genre', attrs={'td': {'style': 'vertical-align: middle'}})
    price = PriceColumn(verbose_name='Price', attrs={'td': {'style': 'vertical-align: middle'}})
    release = tables.DateColumn(verbose_name='Release', attrs={'td': {'style': 'vertical-align: middle'}},
                                format="M j, Y")

    class Meta:
        model = models.Game
        attrs = {'class': 'table table-dark table-hover'}
        row_attrs = {'style': 'transform: rotate(0);'}
        fields = ('avatar', 'title', 'genre', 'price', 'release')
