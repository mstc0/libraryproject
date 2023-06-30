from library import models


def get_profile(req):
    try:
        profile_extra = models.UserExtraProfile.objects.get(user_id=req.user.id)
    except:
        profile_extra = ""
    return {'user_extra': profile_extra}