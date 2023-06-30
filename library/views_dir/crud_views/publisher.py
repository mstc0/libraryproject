from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class PublisherCreateView(CreateView):
    model = models.Publisher
    template_name = 'crud/publisher/publisher-create.html'
    fields = '__all__'
    success_url = reverse_lazy('publisher-create')


class PublisherReadView:
    pass


class PublisherUpdateView(UpdateView):
    model = models.Publisher
    template_name = 'crud/publisher/publisher-update.html'
    fields = '__all__'
    success_url = reverse_lazy('manage')


class PublisherDeleteView(DeleteView):
    model = models.Publisher
    template_name = 'crud/publisher/publisher-delete.html'
    fields = '__all__'
    success_url = reverse_lazy('manage')