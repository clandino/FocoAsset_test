# Sistema de Ventas
### Backend
**Prueba Foco Asset**

Es un sistema que gestiona la venta internacional de productos, utilizando como moneda referente el dólar.
Por defecto el sistema posee lineamientos a seguir específicos para calcular el impuesto de los productos de los siguientes países:
-	China
-	Japón
-	Tailandia
-	Singapur
-	India


## Caracteristicas

---
- Capacidad de crear y visualizar tanto los clientes como los productos
- Manejo de descuentos e impuestos dependiendo del pais
- Visualización de las ventas realizadas y sus detalles para una mejor administración

## Herramientas

---
El sistema fue desarrollado utilizando el lenguaje [Python](https://www.python.org) y aprovecha de las sigueintes librerias:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Framework ligero para un rapido desarrollo.
- [Ponyorm](https://ponyorm.org) - Libreria para manejo de la base de datos.

## Instalación

---
Una vez clonado ó descargado el repositorio cuanta con dos maneras iniciar

1. En caso de querer usar la imagen docker:
    -	Ubicándose dentro de la carpeta del proyecto, montar la imagen ejecutando el comando:
         ```sh
         $ docker build -t foco .
         ```
         > Nota: `foco` es un nombre personalizado para la imagen el cual se puede sustituir por cualquier otro.
    
    -	Para iniciar la imagen se debe ejecutar el comando: 
         ```sh
         $ docker run -it foco bash
         ```
    -	Asegurarse de estar en la carpeta del proyecto `/usr/src/app`
    -	Para iniciar la aplicación se ejecuta el comando: 
         ```sh
         $ flask run
         ```
      1. En caso querer ejecutar de manera local:
          - Ubicarse dentro de la carpeta del proyecto para activar el entorno virtual 
            - En caso de estar usando el sistema Linux debe ejecutar el comando:
              ```sh
              $ source venv/Scripts/actívate
              ```
            - En caso de estar usando el sistema Windows ejecute el comando:
              ```sh
              > venv\Scripts\activate.bat
              ```
          - Ahora que el ambiente virtual esta activo para iniciar la aplicación ejecute el comando:
            ```sh
            > flask run
            ```
El sistema usará el archivo `app.py` para iniciar dentro del `puerto 5000`. El cual puede ser editado para cambiar la naturaleza del proyecto cambiando el valor dentro de la llamada a la función `create_app()`.
-	1 para colocar el sistema de forma normal.
-	2 para colocar el sistema en modo de pruebas.

## Configuración:

---

Todo pais distinto a los cinco generados por defecto han de hacer referencia al impuesto 1.
En caso de querer añadir nuevos lineamientos para un país en concreto se deben seguir los siguientes pasos:
-	Crear una nueva entrada en la tabla impuesto.
-	Asignar en la entrada el tipo de impuesto para especificar si el valor será porcentual o numérico.
-	Añadir una nueva entrada a la tabla país.
-	Asignar a la entrada el número de impuesto creado.
-	Añadir los lineamientos específicos para el nuevo impuesto dentro de la clase calcularIVA.
> Nota: Si se requiere hacer uso de un impuesto existente para un país nuevo, basta con asignar el número de impuesto dentro de la nueva entrada.

## Endpoints

---

#### Ventas

|**Verbo**|**Descripción**|
|---|---|
|**GET** `/buscarVenta/{numero}` | Busca un número de venta segun su id y de encontrarlo lo devuelve al receptor|
|**GET** `/listarVentas` | Obtiene todas las ventas|
|**GET** `/probarImpuesto/{numProducto}/{numCliente}` | Busca un numero de venta segun su id y de encontrarlo lo devuelve al receptor|
|**POST** `/crearVenta` | Procesa los detalles de una venta para generar sus detalles|
|**PUT** `/finalizarVenta` | Calcula los impuestos de la venta y aplica los calculos extras que falten|

##### Detalles

**GET** `/buscarVenta/{numero}`
Busca un numero de venta segun su id y de encontrarlo lo devuelve al receptor
- **Parametros:** 
    numero (int) id de la venta
- **Return:**
    resultado (Venta) la venta encontrada

**GET** `/listarVentas`
 Obtiene todas las ventas
 - **Return:**
    (Json) objeto Json con todas las ventas
 
 **GET** `/probarImpuesto/{numProducto}/{numCliente}` 
Busca un numero de venta segun su id y de encontrarlo lo devuelve al receptor
- **Parametros:**
    numProducto (int): id del producto
    numCliente (int) id del usuario
 - **Return:**
    resultado (float) lo que le toca pagar al usuario

**POST** `/crearVenta`
Procesa los detalles de una venta para generar sus detalles, sirve para poder crear una venta que puede no ser calculada directamente
-	**Return:**
	Venta (venta): la venta con todos sus detalles. 
	(String) Mensaje de fallo

**PUT** `/finalizarVenta`
Funcion que calcula los impuestos de la venta y aplica los calculos extras que falten
-	Return:
	Venta (venta): la venta con todos sus detalles.

#### Cliente
|**Verbo**|**Descripción**|
|---|---|
|**GET** `/listarClientes`| Devuelve todos los clientes dentro de la base de datos|
|**POST** `/ingresarCliente`| Ingresa un cliente nuevo al sistema|

##### Detalles

**GET** `/listarClientes`
Devuelve todos los clientes dentro de la base de datos
- **Return:**
    respuesta (JSON) Todos los clietes encontrados

**POST** `/ingresarCliente`
Ingresa un cliente nuevo al sistema
-    Return:
    (String) Resultado de la transaccion. 

#### Producto
|**Verbo**|**Descripción**|
|---|---|
|**GET** `/listarProductos`| Devuelve todos los produtos dentro de la base de datos|
|**POST** `/ingresarProducto`| Ingresa un producto nuevo al sistema|

##### Detalles

**GET** `/listarProductos`
Devuelve todos los produtos dentro de la base de datos
- **Return:**
    respuesta (JSON) Todos los productos encontrados

**POST** `/ingresarProducto`
Ingresa un producto nuevo al sistema
-    Return:
    (String) Resultado de la transaccion. 
