from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models
from django.contrib.auth.mixins import PermissionRequiredMixin


class GameDeveloperCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_gamedeveloper"
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamedeveloper-create')


class GamePublisherCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_gamepublisher"
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-create.html'
    fields = '__all__'
    success_url = reverse_lazy('gamepublisher-create')


class GameDeveloperUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_gamedeveloper"
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GameDeveloperDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_gamedeveloper"
    model = models.GameDeveloper
    template_name = 'crud/gamedeveloperpublisher/gamedeveloper-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GamePublisherUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_gamepublisher"
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class GamePublisherDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_gamepublisher"
    model = models.GamePublisher
    template_name = 'crud/gamedeveloperpublisher/gamepublisher-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


