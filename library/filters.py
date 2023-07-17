import datetime
import re

import django.forms as forms
import django_filters as df
from django_filters import FilterSet

from .models import Game
from .models import GameFromAPI


class APIGamesFilter(FilterSet):
    title = df.CharFilter(
        label='Title',
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={"class": "form-control text-white bg-dark border-secondary", "max_length": "100"})
    )
    genre = df.CharFilter(
        label='Genre',
        field_name='genre',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={"class": "form-control text-white bg-dark border-secondary", "max_length": "100"})
    )
    price = df.RangeFilter(
        label='Price',
        field_name='price',
    )
    release = df.DateFilter(
        label='Release',
        field_name='release',
        widget=forms.SelectDateWidget(attrs={"class": "form-control text-white bg-dark border-secondary"},
                                      years=range(1962, datetime.datetime.now().year + 1))
    )

    class Meta:
        model = GameFromAPI
        fields = {"title": ["contains"], "price": ["range"], "genre": ["contains"], "release": ["range"]}


class SelectDateWidgetNew(forms.SelectDateWidget):
    re.compile('(\d\d?)/(\d\d?)/(\d{4}|0)$')


class GamesFilter(FilterSet):
    title = df.CharFilter(
        label='Title',
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={"class": "form-control text-white bg-dark border-secondary", "max_length": "100"})
    )
    genre = df.CharFilter(
        label='Genre',
        field_name='genre',
        lookup_expr='name__contains',
        widget=forms.TextInput(attrs={"class": "form-control text-white bg-dark border-secondary", "max_length": "100"})
    )
    price = df.RangeFilter(
        label='Price',
        field_name='price',
    )
    release = df.DateFilter(
        label='Release',
        field_name='release',
        lookup_expr='icontains',
        widget=SelectDateWidgetNew(attrs={"class": "form-control text-white bg-dark border-secondary"},
                                   years=range(1962, datetime.datetime.now().year + 1))
    )

    class Meta:
        model = Game
        fields = {"title": ["contains"], "price": ["range"], "genre": ["contains"], "release": ["range"]}
