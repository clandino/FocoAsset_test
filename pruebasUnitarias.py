import unittest
from datetime import datetime
from typing import Dict

import venta
import clienteProducto
from myFlask import create_app
from datos import *

class TestFoo(unittest.TestCase):
    def setUp(self):
        """ Crea la aplicacion como app de pruebas y popula la base de datos"""
        self.app = create_app(1)
        self.popularBD()
        pass

    def popularBD(self):
        """ Agrega datos falsos para realizar las pruebas"""
        with db_session:
            #Descuentos
            descuento1 = Descuento(descripcion="Otoño",valor=20,tipo=TipoDescuento[1])
            descuento2 = Descuento(descripcion="Viernes Negro",valor=55,tipo=TipoDescuento[1])
            descuento3 = Descuento(descripcion="Verano",valor=10.5,tipo=TipoDescuento[2])
            
            pais = Pais(nombre='Chile',moneda='test1',cambio=1,impuesto=Impuesto[1])   
            
            #Producto
            producto1 = Producto(serial='1',nombre='test1',pais=Pais[1],precio=50)
            producto2 = Producto(serial='2',nombre='test2',pais=Pais[2],precio=10)
            producto3 = Producto(serial='3',nombre='test3',pais=Pais[5],precio=110)
            producto4 = Producto(serial='4',nombre='test4',pais=Pais[3],precio=23.4)
            producto5 = Producto(serial='5',nombre='test5',pais=Pais[4],precio=32.3)
            producto6 = Producto(serial='6',nombre='test6',pais=pais,precio=32.3)

            #Usuarios
            cliente1 = Usuario(identificador='setUp1',clave='bad',correo='setUp1@gmail.com',nombre='usuario set up 1',pais=Pais[1],direccion='test de direccion_prueba 1')
            cliente2 = Usuario(identificador='setUp2',clave='bad',correo='setUp2@gmail.com',nombre='usuario set up 2',pais=Pais[2],direccion='test de direccion_prueba 2')
            cliente3 = Usuario(identificador='setUp3',clave='bad',correo='setUp3@gmail.com',nombre='usuario set up 3',pais=Pais[3],direccion='test de direccion_prueba 3')
            cliente4 = Usuario(identificador='setUp4',clave='bad',correo='setUp4@gmail.com',nombre='usuario set up 4',pais=Pais[4],direccion='test de direccion_prueba 4')
            cliente5 = Usuario(identificador='setUp5',clave='bad',correo='setUp5@gmail.com',nombre='usuario set up 5',pais=pais,direccion='test de direccion_prueba 5')

            Venta(
                precioTotalSinImpuesto=0,
                totalImpuesto=0,
                descuento=None,
                precioTotal=0,
                cliente=Usuario[1],
                fecha=datetime.datetime.now(),
                detalles={}
            )

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)
        pass

    def test_listar_ventas(self):
        """Prueba la busqueda de todos los ventas.

        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """
        with self.app.test_client() as c:
            respuesta = c.get('/listarVentas')
            data = respuesta.data
            self.assertNotEqual(data, None)

    def test_buscar_ventas(self):
        """Prueba la busqueda de una venta en especifico con datos correctos y erroneos.

        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """
        with self.app.test_client() as c:
            rv = c.get('/buscarVenta/1')
            self.assertNotEqual(rv.data, None)
            self.assertFalse(rv.data == "La venta introducida no existe")

    def test_buscar_clientes(self):
        """Prueba la busqueda de todos los clientes.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """
        with self.app.test_client() as c:
            respuesta = c.get('/listarClientes')
            data = respuesta.data
            self.assertNotEqual(data, None)

    def test_buscar_productos(self):
        """Prueba la busqueda de todos los productos.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        
        """
        with self.app.test_client() as c:
            respuesta = c.get('/listarProductos')
            data = respuesta.data
            self.assertNotEqual(data, None)

    @db_session
    def test_buscar_venta(self):
        """Prueba la busqueda de una venta usando datos correctos y erroneos.

        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """

        print(Venta[1].id)
        with self.app.test_client() as c:
            respuesta = c.get('/buscarVenta/' + str(Venta[1].id))
            respuesta2 = c.get('/buscarVenta/-99')
            self.assertNotEqual(respuesta.data, None)
            self.assertIn(b"La venta introducida no existe",respuesta2.data)
    
    @db_session
    def test_probar_impuesto(self):
        """Busca los primeros dos elementos de cliente y producto
        para realizar una prueba y ver cual impuesto se ha de aplicar.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """
        producto = Producto(serial='test123', nombre='productoTest',pais=1,precio=25.4)
        cliente = Usuario[1]
        print(producto)
        print(cliente)
        with self.app.test_client() as c:
            respuesta = c.get('/probarImpuesto/' + str(producto.id) + '/' + str(cliente.id))
            respuesta2 = c.get('/probarImpuesto/-99/-1')
            self.assertNotEqual(respuesta.data, None)
            self.assertIn(b"Verifique los datos introducidos para la consulta",respuesta2.data)

    def test_probar_nuevo_cliente(self):
        """Intenta crear un nuevo usuario y validar que un cliente erroneo no se genere.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local."""
        datos = {
            'usuario': "usuarioTest",
            'clave': "clave",
            'correo': "testunitario@gmail.com",
            'nombre': "test",
            'pais': "Japon",
            'direccion': "direccion_prueba"
        }
        with self.app.test_client() as c:
            respuesta = c.post('/ingresarCliente', data=datos)
            datos["pais"]= "No existe"
            datos["usuario"] = None
            datos["correo"]= None
            respuesta2 = c.post('/ingresarCliente', data=datos)
            self.assertIn(b'Cliente registrado',respuesta.data)
            self.assertIn(b'Conflicto de datos',respuesta2.data)

    def test_probar_nuevo_producto(self):
        """Intenta crear un nuevo producto y validar que un producto erroneo no se genere.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local.
        """
        datos = {
            'serial': "12345",
            'nombre': "pruebaproducto",
            'pais': "Japon",
            'precio': 789863
        }
        with self.app.test_client() as c:
            respuesta = c.post('/ingresarProducto', data=datos)
            datos["pais"]="NOPE"
            datos["serial"]= None
            respuesta2 = c.post('/ingresarProducto', data=datos)
            self.assertIn(respuesta.data, b'Producto registrado')
            self.assertIn(respuesta2.data, b'Conflicto de datos')

    @db_session
    def test_probar_crearVenta(self):
        """Intenta crear varias ventas con tal de probar los diferentes
        tipos de impuestos con diferentes tipos de usuario. Tiene cuatro pruebas que si crearan ventas y 4 que no.
        
        Parametros:
        self (TestFoo) instancia de la clase, con la cual se tiene acceso a la app local
        """
        listaProductosMalos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
        listaProductos = [Producto[1].id,Producto[3].id,Producto[2].id,Producto[2].id, Producto[4].id]
        listaCantidades = [5,10,21,50,30]
        datos = {
            'usuario': str(Usuario[1].id),
            'productos': listaProductos,
            'cantidades': listaCantidades,
            'descuento': str(Descuento[1].id),
            'bandera': True
        }
        with self.app.test_client() as c:
            respuesta1 = c.post('/crearVenta',data=datos)

            datos["usuario"] = str(Usuario[2].id)
            datos["descuento"] = str(Descuento[2].id)
            respuesta2 = c.post('/crearVenta',data=datos)

            datos["usuario"] = str(Usuario[3].id)
            datos["descuento"] = str(Descuento[2].id)
            datos["bandera"] = False
            respuesta3 = c.post('/crearVenta',data=datos)

            datos["usuario"] = str(Usuario[4].id)
            datos["descuento"] = str(Descuento[1].id)
            respuesta4 = c.post('/crearVenta',data=datos)

            datos["usuario"] = "-99"
            datos["descuento"] = str(Descuento[1].id)
            respuesta5 = c.post('/crearVenta',data=datos) #fallo de usuario

            datos["usuario"] = str(Usuario[4].id)
            datos["productos"] = listaProductosMalos
            datos["cantidades"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            respuesta6 = c.post('/crearVenta', data=datos)  # fallo de limite

            datos["productos"] = []
            datos["cantidades"] = []
            respuesta7 = c.post('/crearVenta', data=datos)  # fallo por no data

            datos["productos"] = [1, 2, 3]
            datos["cantidades"] = [1, 2]
            respuesta8 = c.post('/crearVenta', data=datos)  # fallo por discrepancia
            self.assertNotEqual(respuesta1.data, None)
            self.assertNotEqual(respuesta2.data, None)
            self.assertNotEqual(respuesta3.data, None)
            self.assertNotEqual(respuesta4.data, None)
            self.assertIn(b'Conflicto de datos',respuesta5.data)
            self.assertIn(b'La cantidad de productos comprados no puede ser mayor a 20',respuesta6.data)
            self.assertIn(b'No se puede procesar una venta sin productos',respuesta7.data)
            self.assertIn(b'Conflicto en la venta',respuesta8.data)