import json
import os
from urllib.request import urlopen

import django_tables2 as tables
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django_filters.views import FilterView

from library import filters
from library import models, forms
from library import tables as lib_tables


class GameCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_game"
    model = models.Game
    form_class = forms.GameImageForm
    template_name = 'crud/game/game-create.html'
    success_url = reverse_lazy('game-create')


class GameListView(ListView):
    model = models.Game
    template_name = 'crud/game/game-read.html'
    # paginate_by = 3


class GameDetailView(DetailView):
    model = models.Game
    template_name = 'crud/game/game-read-detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = models.Review.objects.all().filter(game_id=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            my_profile = models.UserExtraProfile.objects.get(user=self.request.user)
            my_friends = my_profile.friends.all()
            context["my_friends"] = my_friends
            context["owned_games"] = my_profile.owned_games.all()
            context["wish_list"] = my_profile.wish_list.all()
        return context

    def post(self, request, pk):
        game = models.Game.objects.get(id=pk)
        profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
        if 'add-wishlist' in request.POST and self.request.user.is_authenticated:
            wishlist, created = models.UserWishlist.objects.get_or_create(user=profile, game=game)
            if created:
                wishlist.save()
        if 'remove-wishlist' in request.POST and self.request.user.is_authenticated:
            wishlist, created = models.UserWishlist.objects.get_or_create(user=profile, game=game)
            if not created:
                wishlist.delete()
        return redirect('game-read-detail', pk=pk)


class GameUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_game"
    model = models.Game
    form_class = forms.GameImageForm
    template_name = 'crud/game/game-update.html'
    success_url = reverse_lazy('admin-panel')

    def form_valid(self, form):
        game = models.Game.objects.get(pk=self.kwargs['pk'])
        if game.avatar:
            os.remove(str(game.avatar))
        if game.logo:
            os.remove(str(game.logo))
        return super(GameUpdateView, self).form_valid(form)


class GameDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_game"
    model = models.Game
    template_name = 'crud/game/game-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GamesTableView(tables.SingleTableMixin, FilterView):
    table_class = lib_tables.GamesTable
    queryset = models.Game.objects.all()
    template_name = 'crud/game/game-read2.html'
    paginator_class = tables.LazyPaginator
    filterset_class = filters.GamesFilter


class GamesAPITableView(tables.SingleTableMixin, FilterView):
    table_class = lib_tables.APIGamesTable
    queryset = models.GameFromAPI.objects.all()
    template_name = 'crud/game/game-api-read.html'
    paginator_class = tables.LazyPaginator
    filterset_class = filters.APIGamesFilter


class GameAPIDetailView(DetailView):
    slug_field = "steamid"
    slug_url_kwarg = "steamid"
    model = models.GameFromAPI
    template_name = 'crud/game/game-api-read-detail.html'
    context_object_name = 'game'

    def get(self, *args, **kwargs):
        steamid = self.kwargs['steamid']
        game = models.GameFromAPI.objects.get(steamid=steamid)
        if not game.genre:
            response = urlopen(f'http://store.steampowered.com/api/appdetails?appids={steamid}&cc=us')
            response_json = json.loads(response.read())
            try:
                game_data = response_json[steamid]['data']

                genres = [description['description'] for description in game_data['genres']]
                price = game_data['price_overview']['final'] * 0.01
                if game_data['release_date']['coming_soon']:
                    release = None
                release = game_data['release_date']['date']
                developers = game_data['developers']
                publishers = game_data['publishers']
                logo = game_data['header_image']

                game.genre = ', '.join(genres)
                game.price = price
                game.release = release
                game.developer = ', '.join(developers)
                game.publisher = ', '.join(publishers)
                game.logo = logo
                game.save()
            except KeyError:
                game.delete()
                return redirect('game-api-read')
        return super().get(*args, **kwargs)
