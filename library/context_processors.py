from library import models
from .cart import Cart

def get_profile(req):
    try:
        profile_extra = models.UserExtraProfile.objects.get(user_id=req.user.id)
    except:
        profile_extra = ""
    cart = Cart(req).cart.keys()
    return {'user_extra': profile_extra, 'cart': cart}