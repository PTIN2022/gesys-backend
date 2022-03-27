from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.db import connections # Es algo temporal. 


class Test(APIView):
	products = [
		{'id': 1, 'name': 'Libreta'},
		{'id': 2, 'name': 'Boli'},
		{'id': 3, 'name': 'Lápiz'},
	]

	def get(self, request, format=None):
		return Response(self.products)

	def post(self, request, format=None):
		d = {
			'name': request.data.get('name', '-'),
			'id': len(self.products)+1
		}
		self.products.append(d)
		return redirect(reverse("list_products"))

	def delete(self, request, pk, format=None):
		pos = 0
		for i, item in enumerate(self.products):
			if i['id'] == request.data['id']:
				pos = i
				break
		self.products.remove(pos)

		return redirect(reverse("list_products"))

	def put(self, request, format=None, *args, **kwargs):
		for i in self.products:
			if i['id'] == request.data['id']:
				i['name'] = request.data['name']

		return redirect(reverse("list_products"))


class Login(APIView):
	def post(self, request, format=None):
		# Buscamos el usuario y contraseña que nos pasan por HTTP POST
		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if username is None or password is None:
			return Response({
				'msg': 'Los datos no pueden estar vacíos.' # Mirar de devolver un mensaje más informativo.
			}, status=400)

		# Hacemos la autenticación, verificamos que en la tabla User existe este usuario.
		user = authenticate(username=username, password=password)
		if user is not None: # Y si existe, hacemos el login. Creamos una sesión para éste.
			login(request, user)
			return Response({'msg': 'Autenticado con éxito.'}, status=200)
		else:
			return Response({'msg': 'Credenciales inválidas.'}, status=400)


class Registro(APIView):
	def post(self, request, format=None):
		data = {
			'username': request.data.get('username'),
			'password': request.data.get('password'),
			'first_name': request.data.get('first_name'),
			'last_name': request.data.get('last_name'),
			'email': request.data.get('email'),
			'is_superuser': False,
			'is_staff': True,
			'is_active': True
		}

		# Guardamos los datos del vehículo.
		car_data = {

		}

		# Guardamos los error en el siguiente array.
		errors = []

		if not data['first_name']:
			errors.append({'first_name': 'El nombre es obligatorio.'})
		if not data['last_name']:
			errors.append({'last_name': 'El apellido es obligatorio.'})
		if not data['username']:
			errors.append({'username': 'El nombre de usuario no puede estar vacío.'})
		if not data['password']:
			errors.append({'password': 'La contraseña no puede estar vacía.'})
		if not data['email']:
			errors.append({'email': 'El email es obligatorio.'})

		# Verificamos si el email tiene el formato correcto. Usamos el try porque sino salta un excepción.
		try:
			validate_password(data['email'])
		except:
			errors.append({'email': 'El formato del correo no es correcto.'})

		try:
			validate_password(data['password'])
		except:
			errors.append({'password': 'La contraseña no cumple con los requisitos. Recuerda que debe tener al menos 8 carácteres.'})

		# Miramos si hay errores de comprovación de campos.
		if len(errors):
			return Response({'msg': errors}, status=400)
		else:
			# Vemos la previa existencia del usuario.
			user_exists = User.objects.filter(username=data['username'])
			if user_exists:
				return Response({'msg': 'El usuario ya existe.'}, status=400)

		# Creamos el usuario con los datos proporcionados.
		new_user = User.objects.create_user(**data)
		new_user.save()
		#new_user_id = new_user.id

		# Guardamos el "vehículo" del usuario.
		# TODO

		return Response({'msg': 'Usuario creado con éxito.'}, status=200)