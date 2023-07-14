import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from library import forms, models
from .cart import Cart
# Create your views_dir here.


def test(req):
    cart = Cart(req)
    cart.clear()
    return render(req, template_name='test.html')


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


class ReviewCreateView(CreateView):
    model = models.Review
    fields = ('is_positive', 'review_content',)
    template_name = 'crud/game/game-create-review.html'

    def form_valid(self, form):
        user = models.UserExtraProfile.objects.get(user=self.request.user)
        game = models.Game.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.game = game
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('game-read-detail', kwargs={'pk': self.kwargs['pk']})


def wishlist(request):
    profile = models.UserExtraProfile.objects.get(user=request.user)
    wish_list = models.UserWishlist.objects.all().filter(user=profile).all()
    if 'remove-wishlist' in request.POST:
        wishlist, created = models.UserWishlist.objects.get_or_create(user=profile, game=request.POST['remove-wishlist'])
        if not created:
            wishlist.delete()
    return render(request, template_name='wish-list.html', context={'wishlist': wish_list})
