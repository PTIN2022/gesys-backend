from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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
