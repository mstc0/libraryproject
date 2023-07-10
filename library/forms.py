from django import forms
from library import models
from django.db.transaction import atomic
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.core.files.images import get_image_dimensions


class SignUpForm(UserCreationForm):
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

            if len(avatar) > (40 * 1024):
                raise forms.ValidationError('Avatar file size may not exceed 40k.')

        except AttributeError:
            pass

        return avatar