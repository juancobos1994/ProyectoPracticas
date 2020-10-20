from django.shortcuts import render

from Spider.models import obtener_datos

data=None
productos=None


def mostrar_resutados(request):

	data = enviar_datos()
	productos = obtener_datos(data)
	contexto={'productos':productos}
	return render(request, 'resultados.html', contexto)




