import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from library import forms, models
from .cart import Cart
# Create your views_dir here.


def test(req):
    cart = Cart(req)
    cart.clear()
    return render(req, template_name='test.html')


class ProfileView(View):
    def get(self, req, pk):
        if req.user.id is pk:
            my_profile = models.UserExtraProfile.objects.get(user=req.user)
            games = models.UserOwnedGames.objects.all().filter(user=my_profile)
            return render(req, template_name='my-profile.html', context={'profile': my_profile, 'games': games})
        else:
            user = models.User.objects.get(id=pk)
            user_profile = models.UserExtraProfile.objects.get(user=user)
            return render(req, template_name='user-profile.html', context={'profile': user_profile})


class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


class RegisterCreateView(CreateView):
    success_url = reverse_lazy('login')
    form_class = forms.SignUpForm
    template_name = 'registration/register.html'

class AdminPanel(TemplateView):
    template_name = 'adminpanel.html'
    extra_context = {
        'games': models.Game.objects.all(),
        'genres': models.Genre.objects.all(),
        'developers': models.Developer.objects.all(),
        'publishers': models.Publisher.objects.all(),
    }


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


def cart_purchase(request):
    cart = Cart(request)
    for game in cart.cart:
        game = models.Game.objects.get(id=game)
        user = models.UserExtraProfile.objects.get(user=request.user)
        p = models.UserOwnedGames(game=game, user=user, acquire_date=datetime.datetime.now())
        p.save()
    cart.clear()
    return redirect(reverse_lazy('cart'))
