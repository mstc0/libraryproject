from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class DeveloperCreateView(CreateView):
    model = models.Developer
    template_name = 'crud/developer/developer-create.html'
    fields = '__all__'
    success_url = reverse_lazy('developer-create')


class DeveloperReadView:
    pass


class DeveloperUpdateView(UpdateView):
    model = models.Developer
    template_name = 'crud/developer/developer-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class DeveloperDeleteView(DeleteView):
    model = models.Developer
    template_name = 'crud/developer/developer-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')