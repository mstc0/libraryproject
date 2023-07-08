from library import models
from .cart import Cart

def get_profile(req):
    try:
        profile_extra = models.UserExtraProfile.objects.get(user_id=req.user.id)
    except:
        profile_extra = ""
    return {'user_extra': profile_extra}

def get_cart(req):
    cart = Cart(req)
    return {'cart': cart}