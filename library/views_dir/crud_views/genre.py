from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class GenreCreateView(CreateView):
    model = models.Genre
    template_name = 'crud/genre/genre-create.html'
    fields = '__all__'
    success_url = reverse_lazy('genre-create')


class GenreReadView:
    pass


class GenreUpdateView(UpdateView):
    model = models.Genre
    template_name = 'crud/genre/genre-update.html'
    fields = '__all__'
    success_url = reverse_lazy('manage')


class GenreDeleteView(DeleteView):
    model = models.Genre
    template_name = 'crud/genre/genre-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('manage')