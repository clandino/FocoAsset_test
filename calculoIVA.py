from pony.orm import *
from datos import DetalleVenta

#----------Calculo de impuesto--------------

@db_session
def calculoIva(venta, producto, impuesto):
	""" Funcion que se encarga de buscar el impuesto a aplicar a traves de los lineamientos conocidos para
	cada tipo impuesto. Esto se hara aplicando el dicho lineamiento al precio unitario del producto
	(o detalle de venta si es necesario).
	Parametros:
	venta (Venta): la entidad venta que contiene los detalles requeridos para varios tipos de impuesto
	producto (Producto): la entidad producto a la cual se le aplicara el impuesto
	impuesto (Impuesto): entidad impuesto, de esta se usar el porcenta y tipo para realizar los calculos

	Returns:
	float: el valor de impuesto que se ha de añadir al importe de del detalle venta asociado al producto enviado por parametro
	"""
	resultado = 0
	valor = producto.precioUnitario
	detalleVenta = venta.detalles
	tipo = impuesto.tipo
	porcentaje = impuesto.valor
	if tipo == 1 or tipo > 5: #general: solo se aplica el impuesto porcentual -- aqui van tanto china como los paises fuera de linea
		resultado = calcularPorcentaje(porcentaje, valor)
	if tipo == 2: #porcentaje del mas barato de la compra
		menor = buscarMenor(detalleVenta)
		resultado = calcularPorcentaje(porcentaje, menor)
	if tipo == 3: #porcentaje del mas caro de la compra
		mayor = buscarMayor(detalleVenta)
		resultado = calcularPorcentaje(porcentaje, mayor)
	if tipo == 4: #calculo especial
		if 100 >= valor >= 10:
			resultado = 10
		if 100 <= valor <= 300:
			resultado = 50
	if tipo == 5:# historico
		resultado = -1 #el primer impuesto aplicado no cuenta.
		listaVentas = select(d for d in DetalleVenta if d.pais == producto.pais)[:]
		for v in listaVentas:
			for detalle in v.detalleVenta:
				if detalle.producto.codigo == producto.codigo:
					resultado += 1
		#guardarNuevo valor impuesto
		resultado += 1
	#else
	#	print("No se han establecido reglas para el tipo impuesto ofrecido");
	return resultado

def calcularPorcentaje(porcentaje, valor):
	'''Devuelve el porcentaje calculado '''
	return (porcentaje / 100) * valor

def buscarMenor(lista):
	'''Devuelve el menor precio unitario de toda la venta '''
	menor = lista[0].precioUnitario
	for detalle in lista:
		if menor > detalle.precioUnitario:
			menor = detalle.precioUnitario
	return menor

def buscarMayor(lista):
	'''Devuelve el mayor precio unitario de toda la venta '''
	mayor = lista[0].precioUnitario
	for detalle in lista:
		if mayor < detalle.precioUnitario:
			mayor = detalle.precioUnitario
	return mayor
