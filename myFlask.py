from flask import Flask
from datos import TipoImpuesto, Impuesto, TipoDescuento, db
from venta import *
from clienteProducto import *

def create_app(tipoBD):
    """ Se crea la aplicacion, configurando sus parametros y base de datos
    esto incluye la creacion de datos iniciales en caso de que sea la 
    primera carga de la app
    
    Parametros:
    tipoBD (int) Tipo de base de datos a utilizar

    Return:
    app (Flask) La instancia de flask para el servidor, con sus rutas y blueprints
    """

    app = None
    provider = ''
    filename = ''

    if(tipoBD == 1): #normal
        app = Flask("VentaApp")
        provider = 'sqlite'
        filename = 'database_test.sqlite'
        
    if(tipoBD == 2): #pruebas
        app = Flask("VentaAppTest")
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        provider = 'sqlite'
        filename = ':memory:'
        try:
            db.drop_all_tables(with_all_data=True)
        except BaseException:
            pass
    
    try:
        db.bind(provider, filename, create_db=True)
        db.generate_mapping(create_tables=True)
    except BaseException:
        pass
    
    with db_session:
        if not TipoImpuesto.select().exists(): #si existe ya al menos un dato es porque hice el registro inicial
            #Tipo Descuento
            tipoD1 = TipoDescuento(codigo=1,descripcion="porcentual",tipoValor="porcentual")
            tipoD2 = TipoDescuento(codigo=2,descripcion="numerico",tipoValor="numerico")

            #Tipo Impuesto
            tipoI1 = TipoImpuesto(codigo=1,descripcion="general",tipoValor="porcentual")
            tipoI2 = TipoImpuesto(codigo=2,descripcion="mas barato",tipoValor="porcentual")
            tipoI3 = TipoImpuesto(codigo=3,descripcion="mas caro",tipoValor="porcentual")
            tipoI4 = TipoImpuesto(codigo=4,descripcion="especial",tipoValor="numerico")
            tipoI5 = TipoImpuesto(codigo=5,descripcion="historico",tipoValor="numerico")

            #Impuesto
            impuesto1 = Impuesto(descripcion="General",valor=20,tipo=tipoI1)
            impuesto2 = Impuesto(descripcion="China_general",valor=23.5,tipo=tipoI1)
            impuesto3 = Impuesto(descripcion="India_general",valor=35,tipo=tipoI2)
            impuesto4 = Impuesto(descripcion="Japon_general",valor=25,tipo=tipoI3)
            impuesto5 = Impuesto(descripcion="Tailandia_general",valor=10,tipo=tipoI4)
            impuesto6 = Impuesto(descripcion="Singapur_general",valor=-1,tipo=tipoI5)

            #Paises
            pais1 = Pais(nombre='China',moneda='test1',cambio=1,impuesto=impuesto2)
            pais2 = Pais(nombre='India',moneda='test1',cambio=1,impuesto=impuesto3)
            pais3 = Pais(nombre='Japon',moneda='test1',cambio=1,impuesto=impuesto4)
            pais4 = Pais(nombre='Tailandia',moneda='test1',cambio=1,impuesto=impuesto5)
            pais5 = Pais(nombre='Singapur',moneda='test1',cambio=1,impuesto=impuesto6)

    app.register_blueprint(rutas_ventas)
    app.register_blueprint(rutas_registro)
    return app
