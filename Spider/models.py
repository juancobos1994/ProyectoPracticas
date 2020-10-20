from django.db import models

from bs4 import BeautifulSoup
import requests
import pandas as pd
from Crawler.models import Busqueda, Link

datos=[]


class Producto(models.Model):
	id_busqueda = models.IntegerField()
	id_producto = models.IntegerField()
	titulo = models.CharField(max_length = 200)
	precio = models.CharField(max_length = 20)
	ubicacion = models.CharField(max_length = 50)
	descripcion = models.CharField(max_length = 500)
	url = models.CharField(max_length = 200) 



def datosOlx(link, id_bus, id_pro):
	url = link
	id_busqueda=id_bus
	id_producto=id_pro

	page=requests.get(url)
	soup=BeautifulSoup(page.content, 'html.parser')

	nuevo=[]

	titulos=soup.find_all('h1', class_='_3rJ6e')
	if(len(titulos)>0):
		titulo=titulos[0].text
		titulo=titulo.replace("\n","")
		titulo=titulo.replace("\t","")	
		nuevo.append(titulo)

	precios=soup.find_all('span', class_='_2xKfz')
	if(len(precios)>0):
		precio=precios[0].text
		nuevo.append(precio)

	ubicaciones=soup.find_all('span', class_='_2FRXm')

	if(len(ubicaciones)>0):
		ubicacion=ubicaciones[0].text
		nuevo.append(ubicacion)

	descripciones=soup.find_all('p', class_="")
	
	if(len(descripciones)>0):
		descripcion=""
		for i in descripciones:
			descripcion=descripcion+"\n"+i.text
		nuevo.append(descripcion)

	if(len(nuevo)>0):
		nuevo.append(link)
		datos.append(nuevo)
		producto = Producto(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio, ubicacion=ubicacion, descripcion=descripcion, url=url)
		producto.save()

def datosMercadoLibre(link, id_bus, id_pro):
	
	url = link
	id_busqueda=id_bus
	id_producto=id_pro

	page=requests.get(url)
	soup=BeautifulSoup(page.content, 'html.parser')

	nuevo=[]

	titulos=soup.find_all('h1', class_='item-title__primary')
	titulo=" "
	if(len(titulos)>0):
		titulo=titulos[0].text
		titulo=titulo.replace("\n","")
		titulo=titulo.replace("\t","")
	nuevo.append(titulo)

	precio=" "
	precios=soup.find_all('span', class_='price-tag-fraction')
	if(len(precios)>0):
		precio=precios[0].text
	nuevo.append(precio)

	ubicaciones=soup.find_all('p', class_='gray')
	ubicacion=" "
	if(len(ubicaciones)>0):
		ubicacion=ubicaciones[0].text
	nuevo.append(ubicacion)

	descripciones=soup.find_all('div', class_="item-description__text")
	descripcion=""
	if(len(descripciones)>0):
		for i in descripciones:
			descripcion=descripcion+" "+i.text
	nuevo.append(descripcion)

	if(len(nuevo)>0):
		nuevo.append(link)
		datos.append(nuevo)
		producto = Producto(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio, ubicacion=ubicacion, descripcion=descripcion, url=url)
		producto.save()

def datosAmazon(link, id_bus, id_pro):

	HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

	url = link
	id_busqueda=id_bus
	id_producto=id_pro

	nuevo=[]

	webpage = requests.get(url, headers=HEADERS)

	soup = BeautifulSoup(webpage.content, "lxml")

	title = soup.find_all("span", attrs={"id":'productTitle'})
	titulo=" "
	if(len(title)>0):
		titul=title[0].string
		titulo=titul.replace("\n","")
		titulo=titulo.replace("\t","")
		if(titulo!=" "):
			nuevo.append(titulo)

	price = soup.find_all("span", attrs={'id':'price_inside_buybox'})	
	precio=" "
	if(len(price)>0):
		precio=price[0].string
	nuevo.append(precio)

	ubicaciones=soup.find_all("a", attrs={'id':'sellerProfileTriggerId'})
	ubicacion=" "
	if(len(ubicaciones)>0):
		ubicacion=ubicaciones[0].string
	nuevo.append(ubicacion)

	descripciones=soup.find_all('span', class_="a-list-item")
	descripcion=" "
	if(len(descripciones)>28):
		for i in range(22,27,1):
			descripcion=descripcion+" "+descripciones[i].text
	nuevo.append(descripcion)

	if(len(nuevo)==4):
		nuevo.append(link)
		datos.append(nuevo)
		producto = Producto(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio, ubicacion=ubicacion, descripcion=descripcion, url=url)
		producto.save()

def obtener_datos(df, id_bus):

	cont=0
	for i in df.index: 
		titulo=df["titulo"][i]
		url=df["url"][i]
		pagina=df["pagina"][i]
		cont=cont+1

		if(pagina==0):
			link = Link(id_busqueda = id_bus, id_link=cont, url = url, buscador = 'OLX')
			link.save()
			datosOlx(url, id_bus, cont)

		if(pagina==1):
			link = Link(id_busqueda = id_bus, id_link=cont, url = url, buscador = 'Mercado Libre')
			link.save()
			datosMercadoLibre(url, id_bus, cont)

		if(pagina==2):
			link = Link(id_busqueda = id_bus, id_link=cont, url = url, buscador = 'Amazon')
			link.save()
			datosAmazon(url, id_bus, cont)

	return datos





