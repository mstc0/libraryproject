from django.contrib import admin
from library import models

# Register your models here.
# UserExtraProfile, Game, Genre, GameGenre, Developer, Publisher, GameDeveloperPublisher, UserOwnedGames


admin.site.register(models.UserExtraProfile)
admin.site.register(models.Game)
admin.site.register(models.Genre)
admin.site.register(models.GameGenre)
admin.site.register(models.Developer)
admin.site.register(models.Publisher)
admin.site.register(models.GameDeveloper)
admin.site.register(models.GamePublisher)
admin.site.register(models.UserOwnedGames)
admin.site.register(models.UserWishlist)
admin.site.register(models.FriendRequest)