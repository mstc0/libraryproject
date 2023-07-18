from library import models
from django.core.exceptions import ObjectDoesNotExist
from .cart import Cart

def get_profile(req):
    if req.user.is_authenticated:
        profile_extra, created = models.UserExtraProfile.objects.get_or_create(user_id=req.user.id)
        if created:
            profile_extra.display_name = req.user.username
            profile_extra.save()
        return {'user_extra': profile_extra, 'cart': Cart(req).cart.keys()}
    return {}
