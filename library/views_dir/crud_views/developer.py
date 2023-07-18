from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models
from django.contrib.auth.mixins import PermissionRequiredMixin


class DeveloperCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_developer"
    model = models.Developer
    template_name = 'crud/developer/developer-create.html'
    fields = '__all__'
    success_url = reverse_lazy('developer-create')


class DeveloperUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_developer"
    model = models.Developer
    template_name = 'crud/developer/developer-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class DeveloperDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_developer"
    model = models.Developer
    template_name = 'crud/developer/developer-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')