from pony.orm import *
from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from datos import Usuario, Pais, Producto, Venta
import hashlib

rutas_registro = Blueprint('registro', "registro_blueprint")

@rutas_registro.route('/ingresarCliente', methods=['POST'])
@db_session
def ingresarCliente():
    """ Ingresa un cliente nuevo al sistema
    
    Parametros:
    usuario (str) Identificador del usuario para ingresar al sistema
    clave (str) Password para ingresar al sistema
    correo (str) Correo electronio del cliente
    nombre (str) Nombre real del producto
    pais (str) Nombre del pais al que pertenece
    direccion (str) datos de la direccion del cliente 

    Return:
    (String) Resultado de la transaccion. 
    """
    # POST: Sign user in
    
    if request.method == 'POST':
        if Pais.get(nombre=request.form.get("pais")) is None:
            return "Conflicto de datos"
        pais = Pais.get(nombre=request.form.get("pais"))
        cliente = Usuario(
            identificador=request.form.get('usuario'),
            clave=generate_password_hash(request.form.get('clave'),method='sha256'),
            correo=request.form.get('correo'),
            nombre=request.form.get("nombre"),
            pais=Pais.get(nombre=request.form.get("pais")),
            direccion=request.form.get("direccion")
        )
        cliente.flush()
        if Usuario.get(identificador= request.form.get('usuario')) is None:       
            return "Conflicto de datos"

    return "Cliente registrado"

    
@rutas_registro.route('/ingresarProducto', methods=['POST'])
@db_session
def ingresarProducto():
    """ Ingresa un producto nuevo al sistema
    
    Parametros en request:
    serial (str) Serial del producto
    nombre (str) Nombre real del producto
    pais (str) Nombre del pais al que pertenece
    precio (float) Precio del producto 

    Return:
    (String) Resultado de la transaccion. 
    """
    
    if request.method == 'POST':
        if Pais.get(nombre=request.form.get("pais")) is None:
            return "Conflicto de datos"

        producto = Producto(
            serial = request.form.get('serial'),
            nombre = request.form.get('nombre'),
            pais = Pais.get(nombre=request.form.get("pais")),
            precio = request.form.get('precio')
        )
        if Producto.get(serial= request.form.get('serial')) is None:       
            return "Conflicto de datos"
        
    return "Producto registrado"

@rutas_registro.route('/listarClientes', methods=['GET'])
@db_session
def listarClientes():
    """Devuelve todos los clientes dentro de la base de datos
    
    Return:
    respuesta (JSON) 
    """
    return select(u for u in Usuario)[:].to_json()

@rutas_registro.route('/listarProductos', methods=['GET'])
@db_session
def listarProductos():
    """Devuelve todos los produtos dentro de la base de datos

    Return:
    respuesta (JSON)
    """
    respuesta = select(p for p in Producto)[:].to_json()
    print(len(respuesta))
    return respuesta
