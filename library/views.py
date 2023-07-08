from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View, TemplateView
from library import forms, models
from .cart import Cart
# Create your views_dir here.


def test(req):
    return render(req, template_name='test.html')


def profile(req):
    try:
        profile_extra = models.UserExtraProfile.objects.get(user_id=req.user.id)
    except:
        profile_extra = ""
    return render(req, template_name='profile.html', context={'profile': profile_extra})


class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


class RegisterCreateView(CreateView):
    success_url = reverse_lazy('login')
    form_class = forms.SignUpForm
    template_name = 'registration/register.html'


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


class AdminPanel(TemplateView):
    template_name = 'adminpanel.html'


def cart_add(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(models.Game, id=game_id)
    cart.add(game=game)
    return redirect(reverse_lazy('cart'))


def cart_remove(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(models.Game, id=game_id)
    cart.remove(game=game)
    return redirect(reverse_lazy('cart'))


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})