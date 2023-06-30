from django import forms
from library import models
from django.db.transaction import atomic
from django.contrib.auth.forms import UserCreationForm, ValidationError


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
