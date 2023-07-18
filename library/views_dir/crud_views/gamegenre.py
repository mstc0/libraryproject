from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models
from django.contrib.auth.mixins import PermissionRequiredMixin


class GameGenreCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_gamegenre"
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamegenre-create')


class GameGenreUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_gamegenre"
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GameGenreDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_gamegenre"
    model = models.GameGenre
    template_name = 'crud/gamegenre/gamegenre-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')