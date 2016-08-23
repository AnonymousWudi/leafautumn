# coding=utf-8

from django.contrib import auth
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(required=False)
	password = forms.CharField(required=False, widget=forms.PasswordInput)
	email = forms.EmailField(required=False)

	def clean(self):
		error = False
		user = None

		if not self.cleaned_data['email']:
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if password:
				user = auth.authenticate(username=username, password=password)
				if not user:
					error = True
		else:
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if password:
				users = User.objects.filter(email__iexact=username)
				if not users:
					error = True
				else:
					user = users[0]
					user = auth.authenticate(username=user.username, password=password)
		if user:
			self.user = user
		if error:
			raise forms.ValidationError('')

	def login(self, request):
		if self.is_valid():
			auth.login(request, self.user)
			return True
		return False