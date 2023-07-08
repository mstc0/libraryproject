from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class GameGenreCreateView(CreateView):
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamegenre-create')


class GameGenreReadView:
    pass


class GameGenreUpdateView(UpdateView):
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GameGenreDeleteView(DeleteView):
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')