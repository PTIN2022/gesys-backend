from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, reverse

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
		

