from django.conf import settings
from library import models
from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, game):
        game_id = str(game.id)
        if game_id not in self.cart:
            self.cart[game_id] = {'price': str(game.price)}
            self.save()

    def remove(self, game):
        game_id = str(game.id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        game_ids = self.cart.keys()
        games = models.Game.objects.filter(id__in = game_ids)

        cart = self.cart.copy()
        for game in games:
            cart[str(game.id)]['game'] = game

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        prices = sum(Decimal(item['price']) for item in self.cart.values())
        return prices

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
