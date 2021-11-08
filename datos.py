import datetime
from pony.orm import *

db = Database()

class TipoImpuesto(db.Entity):
    _table_ = "tipo_impuesto"
    codigo = Required(int, unique=True)  # no es auto incrementable
    descripcion = Required(str)
    tipoValor = Required(str)  # porcentual o decimal
    tipo_from = Set("Impuesto", reverse="tipo")

class Impuesto(db.Entity):
    _table_ = "impuesto"
    descripcion = Required(str)
    valor = Required(float)
    tipo = Required(TipoImpuesto, reverse="tipo_from")
    pais_from = Set("Pais", reverse="impuesto")

class Pais(db.Entity):
    _table_ = "pais"
    nombre = Required(str)
    moneda = Required(str)
    cambio = Required(float)
    impuesto = Required(Impuesto, reverse="pais_from")
    pais_from_usuario = Set("Usuario", reverse="pais")
    pais_from_producto = Set("Producto", reverse="pais")
    pais_from_detalle = Set("DetalleVenta", reverse="pais")

class Usuario(db.Entity):
    _table_ = "usuario"
    identificador = Required(str, unique=True)
    clave = Required(str)
    correo = Required(str, unique=True)
    nombre = Required(str)
    pais = Required(Pais, reverse="pais_from_usuario")
    direccion = Required(str)
    cliente_venta = Set("Venta", reverse="cliente")

class Producto(db.Entity):
    _table_ = "producto"
    serial = Required(str, unique=True)
    nombre = Required(str)
    pais = Required(Pais)
    precio = Required(float)
    detalle = Set("DetalleVenta", reverse="producto")

class TipoDescuento(db.Entity):
    _table_ = "tipo_descuento"
    codigo = Required(int, unique=True)  # no es auto incrementable
    descripcion = Required(str)
    tipoValor = Required(str)  # porcentual o decimal
    tipo_from = Set("Descuento", reverse="tipo")

class Descuento(db.Entity):
    _table_ = "descuento"
    descripcion = Required(str)
    valor = Required(float)
    tipo = Required(TipoDescuento,reverse="tipo_from")
    venta = Set("Venta", reverse="descuento")

class Venta(db.Entity):
    _table_ = "venta"
    id = PrimaryKey(int, auto=True)
    precioTotalSinImpuesto = Optional(float)
    totalImpuesto = Optional(float)
    descuento = Optional(Descuento, reverse="venta")
    precioTotal = Optional(float)
    cliente = Required(Usuario, reverse="cliente_venta")
    fecha = Required(datetime.date)
    detalles = Set('DetalleVenta', reverse="detalle_from")
    #detallesVenta = Set("DetalleVenta", reverse="venta")

class DetalleVenta(db.Entity):
    _table_ = "detalle_venta"
    id = PrimaryKey(int, auto=True)
    producto = Required(Producto)
    cantidadVendida = Required(int)
    precioUnitario = Optional(float)
    precioTotalSinImpuesto = Optional(float)
    impuesto = Optional(float)
    precioTotal = Optional(float)
    pais = Required(Pais)
    detalle_from = Set("Venta", reverse="detalles")

with db.set_perms_for(Venta, Producto, TipoImpuesto, TipoDescuento, Impuesto, Pais, Usuario, DetalleVenta, Descuento):
    perm('view create delete', group='anybody')
