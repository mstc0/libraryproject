import os
from library import forms
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import UpdateView, View
from library import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ProfileView(View):
    def get(self, req, pk):
        if req.user.id is pk:
            my_profile = models.UserExtraProfile.objects.get(user=req.user)
            games = models.UserOwnedGames.objects.all().filter(user=my_profile)
            requests_received = models.FriendRequest.objects.all().filter(receiver=my_profile, is_active=True)
            requests_sent = models.FriendRequest.objects.all().filter(sender=my_profile, is_active=True)
            friendlist = my_profile.friends.all()
            self.context = {
                'games': models.Game.objects.all(),
                'genres': models.Genre.objects.all(),
                'developers': models.Developer.objects.all(),
                'publishers': models.Publisher.objects.all(),
            }
            return render(req, template_name='my-profile.html',
                          context={'profile': my_profile,
                                   'games': games,
                                   'friend_requests_received': requests_received,
                                   'friendlist': friendlist,
                                   'friend_requests_sent': requests_sent,
                                   })
        else:
            user = models.User.objects.get(id=pk)
            user_profile = models.UserExtraProfile.objects.get(user=user)
            if self.request.user.is_authenticated:
                my_profile = models.UserExtraProfile.objects.get(user=req.user)
                friend_requests = models.FriendRequest.objects.all()
                is_requested = friend_requests.filter(sender=my_profile, receiver=user_profile, is_active=True).first()
            else:
                my_profile = None
                is_requested = None
            return render(req, template_name='user-profile.html',
                          context={'profile': user_profile,
                                   'is_requested': is_requested,
                                   'my_profile': my_profile})

    def post(self, request, pk):
        if 'accept' in request.POST:
            friend_request = models.FriendRequest.objects.get(id=request.POST['accept'])
            friend_request.accept()
            return redirect(request.META['HTTP_REFERER'])
        elif 'decline' in request.POST:
            friend_request = models.FriendRequest.objects.get(id=request.POST['decline'])
            friend_request.decline()
            return redirect(request.META['HTTP_REFERER'])
        elif 'cancel' in request.POST:
            friend_request = models.FriendRequest.objects.get(id=request.POST['cancel'])
            friend_request.cancel()
            return redirect(request.META['HTTP_REFERER'])
        elif 'cancel2' in request.POST:
            friend_request = models.FriendRequest.objects.get(id=request.POST['cancel2'])
            friend_request.cancel()
            return redirect(request.META['HTTP_REFERER'])
        elif 'unfriend' in request.POST:
            profile = models.UserExtraProfile.objects.get(user=self.request.user)
            user = models.User.objects.get(id=pk)
            user_profile = models.UserExtraProfile.objects.get(user=user)
            profile.unfriend(user_profile)
            return redirect(request.META['HTTP_REFERER'])




class ProfileDisplayUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'crud/profile/display-update.html'
    fields = ('display_name',)
    success_url = reverse_lazy('my-profile')

    def get_object(self, *args, **kwargs):
        return models.UserExtraProfile.objects.get(user_id=self.request.user.id)


class ProfileEmailUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'crud/profile/email-update.html'
    fields = ('email',)
    success_url = reverse_lazy('my-profile')

    def get_object(self, *args, **kwargs):
        return self.request.user


class ProfileAvatarUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'crud/profile/avatar-update.html'
    form_class = forms.AvatarProfileForm

    def get_object(self, *args, **kwargs):
        return models.UserExtraProfile.objects.get(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        user_profile = models.UserExtraProfile.objects.get(user_id=self.request.user.id)
        if user_profile.avatar:
            os.remove(str(user_profile.avatar))
        return super(ProfileAvatarUpdateView, self).form_valid(form)


@login_required
def delete_avatar(request):
    user_profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
    try:
        os.remove(str(user_profile.avatar))
    except:
        pass
    user_profile.avatar = None
    user_profile.save()
    return redirect(reverse_lazy('profile', kwargs={'pk': request.user.id}))


@login_required
def request_friendship(request, pk):
    user_profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
    target_profile = models.UserExtraProfile.objects.get(user_id=pk)
    friend_request, _ = models.FriendRequest.objects.get_or_create(sender=user_profile, receiver=target_profile)
    friend_request.is_active = True
    friend_request.save()
    return redirect(reverse_lazy('profile', kwargs={'pk': pk}))


def my_profile(request):
    profile = models.UserExtraProfile.objects.get(user_id=request.user.id).user.id
    return redirect('profile', pk=profile)

