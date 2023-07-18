from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models
from django.contrib.auth.mixins import PermissionRequiredMixin


class PublisherCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "login.add_publisher"
    model = models.Publisher
    template_name = 'crud/publisher/publisher-create.html'
    fields = '__all__'
    success_url = reverse_lazy('publisher-create')


class PublisherUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_publisher"
    model = models.Publisher
    template_name = 'crud/publisher/publisher-update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')


class PublisherDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_publisher"
    model = models.Publisher
    template_name = 'crud/publisher/publisher-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-panel')