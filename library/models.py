from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.


class UserExtraProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=35, unique=True, validators=[MinLengthValidator(3)])
    owned_games = models.ManyToManyField('Game', through='UserOwnedGames', blank=True, related_name='owned')
    wish_list = models.ManyToManyField('Game', through='UserWishlist', blank=True, related_name='wished')
    avatar = models.ImageField(upload_to='library/static/avatars/', default=None, null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')

    def add_friend(self, target):
        if target not in self.friends.all():
            self.friends.add(target)
            self.save()

    def remove_friend(self, target):
        if target in self.friends.all():
            self.friends.remove(target)
            self.save()

    def unfriend(self, target):
        # removing friend from self list
        remover_friend_list = self
        remover_friend_list.remove_friend(target)
        # removing friend from target list
        target_friend_list = self.objects.get(user=target)
        target_friend_list.remove_friend(self)
        self.save()

    def is_mutual(self, target):
        return target in self.friends.all()

    def __str__(self):
        return f'{self.display_name}'


class Game(models.Model):
    title = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    genre = models.ManyToManyField('Genre', through='GameGenre')
    developer = models.ManyToManyField('Developer', through='GameDeveloper')
    publisher = models.ManyToManyField('Publisher', through='GamePublisher')
    release = models.DateField()

    def __str__(self):
        return f'Game({self.title})'


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Genre({self.name})'


class GameGenre(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'GameGenre({self.game} & {self.genre})'


class Developer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'Developer({self.name})'


class Publisher(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'Publisher({self.name})'


class GameDeveloper(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

    def __str__(self):
        return f'GDP({self.game} & {self.developer})'


class GamePublisher(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return f'GDP({self.game} & {self.publisher})'


class UserOwnedGames(models.Model):
    user = models.ForeignKey(UserExtraProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    acquire_date = models.DateField()

    class Meta:
        unique_together = ('user', 'game')


class UserWishlist(models.Model):
    user = models.ForeignKey(UserExtraProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, unique=True)
    acquire_date = models.DateField()

    class Meta:
        unique_together = ('user', 'game')


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserExtraProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserExtraProfile, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.display_name

    def accept(self):
        if self.receiver:
            self.receiver.add_friend(self.sender)
            if self.sender:
                self.sender.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        # receiver declining
        self.is_active = False
        self.save()

    def cancel(self):
        # sender cancels request
        self.is_active = False
        self.save()


class Review(models.Model):
    user = models.ForeignKey(UserExtraProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_positive = models.BooleanField()
    review_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')