import os
from library import forms
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import UpdateView, View
from library import models


class ProfileView(View):
    def get(self, req, pk):
        if req.user.id is pk:
            my_profile = models.UserExtraProfile.objects.get(user=req.user)
            games = models.UserOwnedGames.objects.all().filter(user=my_profile)
            requests_received = models.FriendRequest.objects.all().filter(receiver=my_profile, is_active=True)
            requests_sent = models.FriendRequest.objects.all().filter(sender=my_profile, is_active=True)
            friendlist = my_profile.friends.all()
            return render(req, template_name='my-profile.html',
                          context={'profile': my_profile,
                                   'games': games,
                                   'friend_requests_received': requests_received,
                                   'friendlist': friendlist,
                                   'friend_requests_sent': requests_sent
                                   })
        else:
            user = models.User.objects.get(id=pk)
            user_profile = models.UserExtraProfile.objects.get(user=user)
            return render(req, template_name='user-profile.html', context={'profile': user_profile})

    def post(self, request, pk):
        if 'accept' in request.POST:
            sender = models.FriendRequest.objects.all().filter(sender=request.POST['accept'])
            sender[0].accept()
            return redirect('profile', pk=request.user.id)
        elif 'decline' in request.POST:
            sender = models.FriendRequest.objects.all().filter(sender=request.POST['decline'])
            sender[0].decline()
            return redirect('profile', pk=request.user.id)
        elif 'cancel' in request.POST:
            print(request.POST['cancel'])
            print(request.POST['cancel'])
            print(request.POST['cancel'])
            print(request.POST['cancel'])
            receiver = models.FriendRequest.objects.all().filter(receiver=request.POST['cancel'])
            receiver[0].cancel()
            return redirect('profile', pk=request.user.id)




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


def request_friendship(request, pk):
    user_profile = models.UserExtraProfile.objects.get(user_id=request.user.id)
    target_profile = models.UserExtraProfile.objects.get(user_id=pk)
    friend_request, _ = models.FriendRequest.objects.get_or_create(sender=user_profile, receiver=target_profile)
    if not _ and not friend_request.is_active:
        friend_request.save()
    else:
        friend_request.is_active = True
        friend_request.save()
    return redirect(reverse_lazy('profile', kwargs={'pk': pk}))

