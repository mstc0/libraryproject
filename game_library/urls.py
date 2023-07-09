"""
URL configuration for game_library project.

The `urlpatterns` list routes URLs to views_dir. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views_dir
    1. Add an import:  from my_app import views_dir
    2. Add a URL to urlpatterns:  path('', views_dir.home, name='home')
Class-based views_dir
    1. Add an import:  from other_app.views_dir import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library import views
from library.views_dir.crud_views import game, genre, gamegenre, gdp, publisher, developer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/update/email', views.ProfileEmailUpdateView.as_view(), name='profile-email-update'),
    path('accounts/profile/update/display', views.ProfileDisplayUpdateView.as_view(), name='profile-display-update'),
    path('accounts/register/', views.RegisterCreateView.as_view(), name='register'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('manage/admin', views.AdminPanel.as_view(), name='admin-panel'),
    path('test', views.test),
    # -- CART --
    path('cart', views.cart_detail, name='cart'),
    path('cart/add/<int:game_id>', views.cart_add, name='cart-add'),
    path('cart/remove/<int:game_id>', views.cart_remove, name='cart-remove'),
    path('cart/purchase', views.cart_purchase, name='cart-purchase'),
    # -- GAME --
    path('manage/game/create', game.GameCreateView.as_view(), name='game-create'),
    path('manage/game/update/<pk>', game.GameUpdateView.as_view(), name='game-update'),
    path('manage/game/delete/<pk>', game.GameDeleteView.as_view(), name='game-delete'),
    path('view/game', game.GameListView.as_view(), name='game-read'),
    path('view/game/<int:pk>', game.GameDetailView.as_view(), name='game-read-detail'),
    # -- GENRE --
    path('manage/genre/create', genre.GenreCreateView.as_view(), name='genre-create'),
    path('manage/genre/update/<pk>', genre.GenreUpdateView.as_view(), name='genre-update'),
    path('manage/genre/delete/<pk>', genre.GenreDeleteView.as_view(), name='genre-delete'),
    # -- GAME_GENRE --
    path('manage/gamegenre/create', gamegenre.GameGenreCreateView.as_view(), name='gamegenre-create'),
    path('manage/gamegenre/update/<pk>', gamegenre.GameGenreUpdateView.as_view(), name='gamegenre-update'),
    path('manage/gamegenre/delete/<pk>', gamegenre.GameGenreDeleteView.as_view(), name='gamegenre-delete'),
    # -- DEVELOPER --
    path('manage/developer/create', developer.DeveloperCreateView.as_view(), name='developer-create'),
    path('manage/developer/update/<pk>', developer.DeveloperUpdateView.as_view(), name='developer-update'),
    path('manage/developer/delete/<pk>', developer.DeveloperDeleteView.as_view(), name='developer-delete'),
    # -- PUBLISHER
    path('manage/publisher/create', publisher.PublisherCreateView.as_view(), name='publisher-create'),
    path('manage/publisher/update/<pk>', publisher.PublisherUpdateView.as_view(), name='publisher-update'),
    path('manage/publisher/delete/<pk>', publisher.PublisherDeleteView.as_view(), name='publisher-delete'),
    # -- GAME_PUBLISHER --
    path('manage/gamepublisher/create', gdp.GamePublisherCreateView.as_view(), name='gamepublisher-create'),
    path('manage/gamepublisher/update/<pk>', gdp.GamePublisherUpdateView.as_view(), name='gamepublisher-update'),
    path('manage/gamepublisher/delete/<pk>', gdp.GamePublisherDeleteView.as_view(), name='gamepublisher-delete'),
    # -- GAME_DEVELOPER --
    path('manage/gamedeveloper/create', gdp.GameDeveloperCreateView.as_view(), name='gamedeveloper-create'),
    path('manage/gamedeveloper/update/<pk>', gdp.GameDeveloperUpdateView.as_view(), name='gamedeveloper-update'),
    path('manage/gamedeveloper/delete/<pk>', gdp.GameDeveloperDeleteView.as_view(), name='gamedeveloper-delete'),
]
