from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from library import models


class GameCreateView(CreateView):
    model = models.Game
    template_name = 'crud/game/game-create.html'
    fields = '__all__'
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
        my_profile = models.UserExtraProfile.objects.get(user=self.request.user)
        my_friends = my_profile.friends.all()
        context["my_friends"] = my_friends
        context["owned_games"] = my_profile.owned_games.all()
        context["wish_list"] = my_profile.wish_list.all()
        return context

    def post(self, request, pk):
        game = models.Game.objects.get(id=pk)
        profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
        owned = models.UserWishlist(user=profile, acquire_date=datetime.now(), game=game)
        owned.save()
        return redirect('game-read-detail', pk=pk)


class GameUpdateView(UpdateView):
    model = models.Game
    template_name = 'crud/game/game-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GameDeleteView(DeleteView):
    model = models.Game
    template_name = 'crud/game/game-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')