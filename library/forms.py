from django import forms
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.core.files.images import get_image_dimensions
from django.db.transaction import atomic

from library import models


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'display_name']

    display_name = forms.CharField(max_length=35, min_length=3)
    email = forms.EmailField(required=True)

    def clean_display_name(self):
        display_name = self.cleaned_data['display_name']
        if models.UserExtraProfile.objects.filter(display_name=display_name).exists():
            raise ValidationError("Display name already taken")
        return display_name

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        display_name = self.cleaned_data['display_name']
        profile = models.UserExtraProfile(display_name=display_name, user=result)
        if commit:
            profile.save()
        return result


class AvatarProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = models.UserExtraProfile
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)
            max_w = max_h = 200
            if w > max_w or h > max_h:
                raise forms.ValidationError(f'Please use image that is {max_w}x{max_h} or smaller')

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']):
                raise forms.ValidationError(f'Only JPG or PNG are allowed.')

            if len(avatar) > (128 * 1024):
                raise forms.ValidationError('Avatar file size may not exceed 128k.')

        except AttributeError:
            pass

        return avatar


class GameImageForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)
    logo = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = models.Game
        fields = "__all__"

    def clean_logo(self):
        logo = self.cleaned_data['logo']

        try:
            w, h = get_image_dimensions(logo)
            max_w = 800
            max_h = 500
            if w > max_w or h > max_h:
                raise forms.ValidationError(f'Please use image that is {max_w}x{max_h} or smaller')

            main, sub = logo.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']):
                raise forms.ValidationError(f'Only JPG or PNG are allowed.')

            if len(logo) > (1024 * 1024):
                raise forms.ValidationError('Logo file size may not exceed 1MB.')

        except AttributeError and TypeError:
            pass

        if logo:
            return logo

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)
            max_w = max_h = 100
            if w > max_w or h > max_h:
                raise forms.ValidationError(f'Please use image that is {max_w}x{max_h} or smaller')

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']):
                raise forms.ValidationError(f'Only JPG or PNG are allowed.')

            if len(avatar) > (128 * 1024):
                raise forms.ValidationError('Avatar file size may not exceed 128k.')

        except AttributeError and TypeError:
            pass

        if avatar:
            return avatar
