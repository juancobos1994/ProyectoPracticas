from django.shortcuts import render

from django.shortcuts import render
from Crawler.models import CrawlerWeb
from .models import Busqueda, Link
from pandas import DataFrame

from Spider.models import obtener_datos

# Create your views here.
diccionario = {'ml':'Mercado Libre', 'olx':'OLX', 'amz':'Amazon'}
def sitios(clave, busqueda, n_pag=1):
    crawler =  CrawlerWeb()
    crawler.newDriver()
    def olx():
        df = crawler.e_commerceOLX(key=busqueda , n_result=n_pag)
        df['pagina']=0
        return df
    def mercadolibre():
        crawler.setUrl('https://listado.mercadolibre.com.ec/')
        crawler.setElement(by='as_word', findby=0)
        df = crawler.e_commerceML( keys=[busqueda] ,n_result=n_pag)
        df['pagina']=1
        return df
    def amazon():
        crawler.setUrl('https://www.amazon.com/-/es/')
        crawler.setElement(by='field-keywords', findby=0)
        df = crawler.e_commerceAmz( keys=[busqueda], n_result=n_pag)
        df['pagina']=2
        return df
    guia ={'ml':mercadolibre, 'olx':olx, 'amz':amazon}
    return guia[clave]()

def buscarid():

	historia = Busqueda.objects.all()

	if(len(historia)==0):
		return 1
	else:
		valor = len(historia) + 1
		return valor

def iniciar(request):
    crawler =  CrawlerWeb()
    if request.method == 'POST':
        paginas = request.POST.getlist('check')
        texto = request.POST.get('q')
        n_pag = int(request.POST.get('links'))
        if not paginas:
            paginas = ['ml','olx','amz']
        df = DataFrame(columns=['titulo','url','pagina'])
        for elem in paginas:
            dfaux = sitios(elem, texto, n_pag)
            df = df.append(dfaux, ignore_index=True)
        print("total: ", df.shape)
        #dataframe total df
        sitio = ', '.join([diccionario[e] for e in paginas])

        id_busqueda=buscarid()

        busqueda = Busqueda(id_busqueda=id_busqueda, texto=texto, n_paginas =n_pag, sitios =sitio)
        busqueda.save()
        productos = obtener_datos(df, id_busqueda)
        contexto={'productos':productos}
        return render(request, 'resultados.html', contexto)
    else:
        return render(request, 'index.html')

def historial(request):
    historia = Busqueda.objects.all()
    contexto = {"elementos": historia}
    return render(request, 'historial.html', contexto)

