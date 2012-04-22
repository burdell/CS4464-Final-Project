from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django import forms

#models
class UserProfile(models.Model):
	user = models.OneToOneField(User)

class MapPost(models.Model):
	lat = models.DecimalField(max_digits=30, decimal_places=10)
	lon = models.DecimalField(max_digits=30, decimal_places=10)
	text = models.CharField(max_length=200)

#forms
class RegistrationForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	username = forms.CharField()
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username):
			raise ValidationError("Username already exists!")
		return username


