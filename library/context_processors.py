from library import models
from .cart import Cart

def get_profile(req):
    cart = Cart(req).cart.keys()
    try:
        profile_extra = models.UserExtraProfile.objects.get(user_id=req.user.id)
        # owned_games = profile_extra.owned_games.all()
        # wish_list = profile_extra.wish_list.all()
    except:
        profile_extra = ""

    return {'user_extra': profile_extra, 'cart': cart}