from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models
from django.contrib.auth.mixins import PermissionRequiredMixin


class GenreCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_genre"
    model = models.Genre
    template_name = 'crud/genre/genre-create.html'
    fields = '__all__'
    success_url = reverse_lazy('genre-create')


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_genre"
    model = models.Genre
    template_name = 'crud/genre/genre-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_genre"
    model = models.Genre
    template_name = 'crud/genre/genre-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')