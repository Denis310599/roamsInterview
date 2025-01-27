# Roams Technical Interview

Este repositorio contiene el codigo corresponidente a una API Rest cuyo propósito es realizar simulaciones de hipoteca. Ha sido desarrollada en Python, utilizando Flask.


## Instrucciones de instalación
##### 0. Clonación del repositorio
Comenzamos por clonar el repositorio en nuetra máquina.

    git clone https://github.com/Denis310599/roamsInterview.git
    cd roamsInterview
##### 1. Instalación de dependencias
Este proyecto ha sido desarrollado utilizando **python 3.12.8**. Utiliza una serie de librerías detalladas en requirements.txt. Para instalar las dependencias necesarias, ejecutar el siguiente comando:

    pip install -r ./requirements.txt

##### 2. Variables de entorno
Será necesario crear una variable de entorno llamada **JWT_SECRET_KEY** necesaria para la autenticación. Esto se puede lograr de la siguiente forma:

    #Windows
    set JWT_SECRET_KEY=my-very-secret-key
    
    #Linux
    export JWT_SECRET_KEY=my-very-secret-key

##### 3. Crear la base de datos
Esta api cuenta con una base de datos, haciendo uso de **SQLite**. Para crear y rellenar las tablas con información básica, se debe ejecutar el siguiente comando:

    flask db create
    flask db populate




## Uso de la API
En este repositorio se puede encontrar la documentación para el uso de la API en el documento [apiDoc.html](./doc/apiDoc.html).

La API se ha probado en Postman, y se dispone del [postman_collection.json](./doc/roams_doc.postman_collection.json) el cual permite importar las llamadas realizadas para el testeo junto con la documentación generada a Postman.

La api se puede arrancar mediante el siguiente comando:

    flask --app app run
  
Una vez arrancada, es necesario iniciar sesión en ella. Para ello se realiza una llamada a http://127.0.0.1:5000/user/login con el siguiente contenido:

    {
      "usuario": "user",
      "contra": "1234"
    }

Esto devolverá una respuesta similar a:

    {
      "token": "<bearer-token>"
    }
Copiamos **\<bearer-token\>** y lo establecemos en la cabecera de Authorization, siendo esta de tipo Bearer Token. A partir de este momento podremos utilizar todas las funciones disponibles de la API.