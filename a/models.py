from django.db import models
from django.http import HttpResponseRedirect
from multiselectfield import MultiSelectField
from decimal import Decimal
from django.conf import settings
from datetime import date
from datetime import datetime

class Categoria(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Marca(models.Model):
	name = models.CharField(max_length=50)
	categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Articulo(models.Model):
	name = models.CharField(max_length=50)
	precio = models.CharField(max_length=10)
	descripcion = models.TextField()
	oferta = models.CharField(max_length=3)
	marca = models.ForeignKey(Marca,on_delete=models.CASCADE)
	masVendido = models.BooleanField(default=False)
	count_vendido = models.CharField(max_length=10,default=0)
	img_mostrador = models.ImageField(upload_to="Producto_mostrador",default="https://st3.depositphotos.com/2927609/32461/v/600/depositphotos_324611040-stock-illustration-no-image-vector-icon-no.jpg")
	newProduct = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def descuento(self):
		precio = float(self.precio)
		porcentaje = float(self.oferta)

		total_descuento = precio * (porcentaje / 100 )
		return total_descuento



class Tamanio(models.Model):
	TAMANIO_CHOICES = (
	    ('xl','XL'),
	    ('l', 'L'),
	    ('md','MD'),
	    ('m','M'),
	    ('s','S'),
	    ('xs','XS'),
	)
	articulo = models.OneToOneField(Articulo, default=None,on_delete=models.CASCADE,null=True,blank=True)
	tamanio = MultiSelectField(max_length=50, choices=TAMANIO_CHOICES, default="xl",null=True,blank=True)

	def __Str__(self):
		return self.articulo.name

class Color(models.Model):
	COLOR_CHOICES = (
	    ('green','VERDE'),
	    ('blue', 'AZUL'),
	    ('red','ROJO'),
	    ('orange','ANARANJADO'),
	    ('black','NEGRO'),
	    ('pink','ROSA'),
	)

	articulo = models.OneToOneField(Articulo, default=None,on_delete=models.CASCADE,null=True,blank=True)
	color = MultiSelectField(max_length=700, choices=COLOR_CHOICES, default='green',null=True,blank=True)

	def __Str__(self):
		return self.articulo.name

class Imagenes(models.Model):
	articulo = models.ForeignKey(Articulo,on_delete=models.CASCADE)
	img = models.ImageField(upload_to="Productos",null=True,blank=True)
	

	def __Str__(self):
		return self.articulo.name


class Consecutive(models.Model):
	number = models.CharField(max_length=20)

class Client(models.Model):
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	email = models.EmailField()
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	password = models.CharField(max_length=18)


	def __Str__(self):
		return self.email


class Order(models.Model):
	consecutive = models.CharField(max_length=2)
	name = models.CharField(max_length=50)
	price = models.CharField(max_length=10)
	quanty = models.CharField(max_length=7)
	discount = models.CharField(max_length=3)
	fecha = models.CharField(max_length=10,default=date.today())
	condition = models.CharField(max_length=20,default="received")
	client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
	methodPaymet = models.CharField(max_length=40,default="Contra Entrega")

	def discountArticle(self):
		price = float(self.price)
		discount = float(self.discount)
		total_discount =price * (discount / 100 )
		return total_discount

	def total(self):
		return float(self.price) * float(self.quanty)




class Carrito(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def add(self,producto,cantidad = 0):
		try:
			self.cart[str(producto.pk)]
		except KeyError as e:
			self.request.session['carrito'] += 1
			
		total = ((float(producto.precio) - float(producto.descuento())) * float(cantidad))
		self.cart[str(producto.pk)] = {'codigo':producto.pk,'articulo':producto.name,'cantidad':cantidad,'precio':producto.precio,'oferta':producto.descuento(),'total':total,'img':producto.img_mostrador.url,
											'description':producto.descripcion
										}
		self.save()
		print(self.cart)

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Articulo.objects.filter(id__in=product_ids)

		for item in self.cart.values():
			yield item


	def __len__(self):
		return sum(item['cantidad'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True











