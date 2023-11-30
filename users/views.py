from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse


from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from users.models.form import PasswordChangeFormCustom

import logging
logger = logging.getLogger('django')


# Create your views here.

def home(request):
	context = {}
	return render(request, "users/home.html", context)

def status(request):
	return HttpResponse("Funciona")


def welcome(request):
	if request.user.is_authenticated:
		return render(request, "users/welcome.html")

	return redirect(reverse("users:login"))


@login_required
def register(request):
	if request.user.id != 1:
		return redirect(reverse("users:login"))

	form = UserCreationForm()
	if request.method == "POST":
		# Añadimos los datos recibidos al formulario
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			user = form.save()

			# Si el usuario se crea correctamente 
			if user is not None:
				# Hacemos el login manualmente
				#do_login(request, user)
				return redirect('/')

	return render(request, "users/register.html", {'form': form})


@login_required
def password(request):
	context = {}

	if request.method == 'POST':
		form = PasswordChangeFormCustom(user=request.user, data=request.POST)

		if form.is_valid():
			form.save()
			# so that user does not get logged out, not working as of now.
			# TODO
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Cambio clave exitoso', extra_tags='Cambio Clave')
			return redirect('/')
		else:
			messages.error(request, 'Error', extra_tags='Cambio Clave')
			return render(request, "users/password.html", {'form': form})

	else:
		form = PasswordChangeFormCustom(user=request.user)
		context['form'] = form
		return render(request, 'users/password.html', context)


def login(request):
	form = AuthenticationForm()
	if request.method == "POST":
		# Añadimos los datos recibidos al formulario
		form = AuthenticationForm(data=request.POST)

		if form.is_valid():
			# Recuperamos las credenciales validadas
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			# Verificamos las credenciales del usuario
			user = authenticate(username=username, password=password)

			# Si existe un usuario con ese nombre y contraseña
			if user is not None:
				# Hacemos el login manualmente
				do_login(request, user)
				messages.success(request, 'Inicio sesion exitoso', extra_tags='Inicio Sesion')
				# Y le redireccionamos a la portada
				return redirect('/')
			else:
				messages.error(request, 'Credenciales invalidas', extra_tags='Inicio Sesion')
		else:
			messages.error(request, 'Credenciales invalidas', extra_tags='Inicio Sesion')

	return render(request, "users/login.html", {'form': form})


@login_required
def logout(request):
	do_logout(request)
	return redirect('/')
