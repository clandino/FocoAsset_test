# Ingreso de venta
import datetime
from flask import Blueprint, request
from calculoIVA import calcularPorcentaje, calculoIva
from datos import Venta, DetalleVenta, Producto, Usuario, Descuento, Pais
from pony.orm import db_session

rutas_ventas = Blueprint('ventas', "venta_blueprint")


@rutas_ventas.route('/listarVentas', methods=['GET'])
@db_session
def listarVentas():
    datos = (Venta.select(lambda v: v))
    return datos.to_json()


@rutas_ventas.route('/buscarVenta/<numero>', methods=['GET'])
@db_session
def buscarVenta(numero):
	""" Busca un numero de venta segun su id y de encontrarlo lo devuelve al receptor

	Parametros:
	numero (int) parametro de busqueda

	Return:
	resultado (Venta) la venta encontrada
	"""
	resultado = Venta.get(id=int(numero))
	if(resultado != None):
		return resultado.to_json()
	return "La venta introducida no existe"


@rutas_ventas.route('/probarImpuesto/<numProducto>/<numCliente>', methods=['GET'])
@db_session
def probarImpuesto(numProducto,numCliente):
	""" Busca un numero de venta segun su id y de encontrarlo lo devuelve al receptor

	Parametros:
	numProducto (int) parametro de busqueda
	numCliente (int) parametro de busqueda

	Return:
	resultado (float) lo que le toca pagar al usuario
	"""
	producto = Producto.get(id=numProducto)
	cliente = Usuario.get(id=numCliente)
	if(producto == None or cliente == None):
		return "Verifique los datos introducidos para la consulta"
	detalles = [producto]
	if(cliente.pais == producto.pais):
		return "0"
	return str(calculoIva(detalles, producto))
	

@rutas_ventas.route('/crearVenta', methods=['POST'])
@db_session
def crearVenta():
	""" Procesa los detalles de una venta para generar sus detalles
	la funcion sirve para poder crear una venta que puede no ser calculada directamente
	
	Parametros:
	cliente (Usuario)
	productos (Producto[]) : lista de productos comprados
	cantidades (int[]) : lista de cantidades compradas de cada producto
	bandera (bool): bandera que indica si la venta se guardara para mas tarde o si sera calculada directamente
	
	Return:
	Venta (venta): la venta con todos sus detalles. 
	(String) Mensaje de fallo
	"""
	#primero creo las variables
	try:
		if request.method == 'POST':
			productos = request.form.getlist("productos")
			cantidades = request.form.getlist("cantidades")
			if(len(productos) != len(cantidades)):
				return "Conflicto en la venta"
			if(len(productos) > 20):
				return "La cantidad de productos comprados no puede ser mayor a 20"
			if(len(productos) == 0):
				return "No se puede procesar una venta sin productos"
			bandera = request.form.get("bandera")
			venta = Venta(
				precioTotalSinImpuesto = 0,
				totalImpuesto = 0,
				descuento = Descuento[int(request.form.get("descuento"))],
				precioTotal = 0,
				cliente = Usuario[int(request.form.get('usuario'))],
				fecha = datetime.datetime.now(),
				detalles = {}
			)
			venta.flush()
	except:
		return "Conflicto de datos"
	#establezco los detalles dentro de la venta
	for x in range(len(productos)):
		producto_base = Producto[productos[x]]
		precio_base: float = producto_base.precio
		pais_base = producto_base.pais
		detalle = DetalleVenta(
			producto=producto_base,
			cantidadVendida=cantidades[x],
			precioUnitario=precio_base,
			precioTotalSinImpuesto=precio_base * int(cantidades[x]),
			impuesto=0,
			precioTotal=0,
			pais=pais_base
		)
		detalle.flush()
		detalle.venta = venta
		venta.precioTotalSinImpuesto += detalle.precioTotalSinImpuesto

	#guardar venta
	if(bandera):
		return finalizarVenta(venta.cliente, venta.id)
	return venta.to_json()


@rutas_ventas.route('/finalizarVenta', methods=['PUT'])
@db_session
def finalizarVenta(numCliente,numVenta):
	"""Funcion que calcula los impuestos de la venta y aplica los calculos extras que falten
	
	Parametros:
	numCliente (Usuario)
	numVenta (Venta.id)

	Return:
	Venta (venta): la venta con todos sus detalles.
	"""
	#obtengo los datos
	if numCliente != None and numVenta != None:
		cliente = Usuario.get(id=numCliente.id)
		venta = Venta.get(id=numVenta)
	else:
		cliente = Usuario.get(id=numCliente.id)
		venta = Venta.get(id=numVenta)
	#calculo los detalles
	contadorPaises = []
	aplicarDescuentoImpuesto = False
	detallesVentas = venta.detalles
	venta.fecha = datetime.date.today()

	#buscar si un mismo pais se repite varias veces
	for detalle in detallesVentas:
		contadorPaises.append(detalle.pais.codigo)
		if(contadorPaises.count(detalle.pais.codigo) >= 5):
			aplicarDescuentoImpuesto = True
			break

	for detalle in detallesVentas:
		ivaCalculado = 0
		#No se aplica descuento cuando el cliente es del pais del producto
		if(detalle.producto.pais != cliente.pais):
			ivaCalculado = calculoIva(detallesVentas, detalle.producto)
		detalle.impuesto = ivaCalculado
		#agregar el descuento de impuesto si hace falta
		if(aplicarDescuentoImpuesto):
			detalle.impuesto -= calcularPorcentaje(10, detalle.impuesto)
		#calculo del total tomando en cuenta el impuesto
		detalle.precioTotal = (ivaCalculado + detalle.precioUnitario) * detalle.cantidadVendida
		#agregar a la venta los totales
		venta.totalImpuesto += detalle.totalImpuesto
		venta.precioTotal += detalle.precioTotal
	#calculo el descuento segun el tipo, 1 es importe, 2 es porcentual
	if(venta.descuento.tipo.codigo == 1):
		venta.precioTotal -= venta.descuento.valor
	if(venta.descuento.tipo.codigo == 2):
		venta.precioTotal -= calcularPorcentaje(venta.descuento.valor, venta.precioTotal)

	return venta.to_json()
