import datetime
import os
from library import forms
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from library import models


class ProfileDisplayUpdateView(UpdateView):
    template_name = 'crud/profile/display-update.html'
    fields = ('display_name',)
    success_url = reverse_lazy('profile')

    def get_object(self):
        return models.UserExtraProfile.objects.get(user_id=self.request.user.id)


class ProfileEmailUpdateView(UpdateView):
    template_name = 'crud/profile/email-update.html'
    fields = ('email',)
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfileAvatarUpdateView(UpdateView):
    template_name = 'crud/profile/avatar-update.html'
    form_class = forms.AvatarProfileForm

    def get_object(self):
        return models.UserExtraProfile.objects.get(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        user_profile = models.UserExtraProfile.objects.get(user_id=self.request.user.id)
        if user_profile.avatar:
            os.remove(str(user_profile.avatar))
        return super(ProfileAvatarUpdateView, self).form_valid(form)



def delete_avatar(request):
    user_profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
    try:
        os.remove(str(user_profile.avatar))
    except:
        pass
    user_profile.avatar = None
    user_profile.save()
    return redirect(reverse_lazy('profile', kwargs={'pk': request.user.id}))
