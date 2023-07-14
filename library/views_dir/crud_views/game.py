import os
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from library import models, forms


class GameCreateView(CreateView):
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
        my_profile = models.UserExtraProfile.objects.get(user=self.request.user)
        my_friends = my_profile.friends.all()
        context["my_friends"] = my_friends
        context["owned_games"] = my_profile.owned_games.all()
        context["wish_list"] = my_profile.wish_list.all()
        return context

    def post(self, request, pk):
        game = models.Game.objects.get(id=pk)
        profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
        if 'add-wishlist' in request.POST:
            wishlist, created = models.UserWishlist.objects.get_or_create(user=profile, game=game)
            if created:
                wishlist.save()
        if 'remove-wishlist' in request.POST:
            wishlist, created = models.UserWishlist.objects.get_or_create(user=profile, game=game)
            if not created:
                wishlist.delete()
        return redirect('game-read-detail', pk=pk)


class GameUpdateView(UpdateView):
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


class GameDeleteView(DeleteView):
    model = models.Game
    template_name = 'crud/game/game-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')