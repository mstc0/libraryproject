import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from library import forms, models
from .cart import Cart


# Create your views_dir here.


def test(req):
    return render(req, template_name='test.html')


class Home(TemplateView):
    template_name = 'home.html'


class About(TemplateView):
    template_name = 'about.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


class RegisterCreateView(CreateView):
    success_url = reverse_lazy('login')
    form_class = forms.SignUpForm
    template_name = 'registration/register.html'


class AdminPanel(PermissionRequiredMixin, TemplateView):
    permission_required = "library.add_developer"
    template = 'adminpanel.html'

    def get(self, request, *args, **kwargs):
        self.context = {
            'games': models.Game.objects.all(),
            'genres': models.Genre.objects.all(),
            'developers': models.Developer.objects.all(),
            'publishers': models.Publisher.objects.all(),
        }
        return render(request, self.template, self.context)


@login_required
def cart_add(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(models.Game, id=game_id)
    cart.add(game=game)
    return redirect(reverse_lazy('cart'))


@login_required
def cart_remove(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(models.Game, id=game_id)
    cart.remove(game=game)
    return redirect(reverse_lazy('cart'))


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def cart_purchase(request):
    cart = Cart(request)
    for game in cart.cart:
        game = models.Game.objects.get(id=game)
        user = models.UserExtraProfile.objects.get(user=request.user)
        p = models.UserOwnedGames(game=game, user=user, acquire_date=datetime.datetime.now())
        p.save()
    cart.clear()
    return redirect(reverse_lazy('cart'))


class ReviewCreateView(LoginRequiredMixin, CreateView):
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


@login_required
def wishlist(request):
    profile = models.UserExtraProfile.objects.get(user=request.user)
    wish_list = models.UserWishlist.objects.all().filter(user=profile).all()
    if 'remove-wishlist' in request.POST:
        wishlist, created = models.UserWishlist.objects.get_or_create(user=profile,
                                                                      game=request.POST['remove-wishlist'])
        if not created:
            wishlist.delete()
    return render(request, template_name='wish-list.html', context={'wishlist': wish_list})


@permission_required("library.add_developer")
def pull_games_from_api(request):
    from urllib.request import urlopen
    import json

    response = urlopen("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    response_json = json.loads(response.read())
    steam_games = {}

    for element in response_json['applist']['apps']:
        steam_games[str(element['appid'])] = element['name']

    for steamid in steam_games.keys():
        game, _ = models.GameFromAPI.objects.get_or_create(title=steam_games[steamid], steamid=steamid)
        if _:
            game.save()

    return redirect('admin-panel')


@login_required
def reviews(request):
    profile = models.UserExtraProfile.objects.get(user=request.user)
    reviews = models.Review.objects.all().filter(user=profile).all()
    if 'remove-review' in request.POST:
        review, created = models.Review.objects.get_or_create(user=profile, game=request.POST['remove-wishlist'])
        if not created:
            review.delete()
    return render(request, template_name='my-reviews.html', context={'reviews': reviews})
