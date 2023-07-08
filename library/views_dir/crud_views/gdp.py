from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class GameDeveloperCreateView(CreateView):
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamedeveloper-create')


class GamePublisherCreateView(CreateView):
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamepublisher-create')



class GDPReadView:
    pass


class GameDeveloperUpdateView(UpdateView):
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GameDeveloperDeleteView(DeleteView):
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GamePublisherUpdateView(UpdateView):
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GamePublisherDeleteView(DeleteView):
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


