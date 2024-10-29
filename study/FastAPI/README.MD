# FastAPI
Es un framework de Python que permite realizar aplicaciones fácilmente. Se caracteriza por ser muy rápido, gracias a su agilidad en el desarrollo, ya que utiliza Types y se basa en estándares de OpenAPI y Swagger, ampliamente respaldado por la comunidad.

## Endpoints
Mediante la instancia de una aplicación de FastAPI.
```python
    app = FastAPI()
```
Y un decorador cual tiene un atributo (método http) con path (url del endpont) hacia una función.
```python
    #Decorador.atributo(path)
    #def funcion () -> tipo_retorno:
    #   ...contenido de función...
    #   return tipo_retorno_mencionado.
    @app.get('/hello_word')
    def hello_world() -> str:
        return 'hello world'
```
### Endpoints con variables en el path.
Se tiene presente lo mismo, la instancia de una aplicación FastApi, pero en la estrucutra del endpoint anterior se agrega en el path "{}" que contienen la variable.
```python
    #Decorador.atributo(path/{variable_de_entrada})
    #def funcion (variable_de_entrada:tipo_variable_de_entrada) -> tipo_retorno:
    #   ...contenido de función donde se puede usar
    #   la variable de entrada en todo el endpoint...
    #   return tipo_retorno_mencionado.
    @app.get('hello_word/{var}')
    def hello_world(var:str) -> str:
        return f'hello world{var}'
```
Nota1: si la variable de entrada no es del tipo que se estipula en los parametros de la función FastAPI, saca error.
Nota2: El nombre de la variable debe ser el mismo en el path como en el parametro de la función decorada.
### Endpoints con query params
Se mantiene la estructura inicial del primer endpoint que vimos sólo que se ubican tantos parametros en la función como querry params se esperen con su respectivo tipo. Se puede usar la función Body() de FastAPI para apuntar que el querry params venga del payload de la request.
```python
    #Decorador.atributo(path)
    #def funcion (querry_param:tipo_querry_param = donde_sacarlo) -> tipo_retorno:
    #   ...contenido de función...
    #   return tipo_retorno_mencionado.
    @app.get('/hello_word')
    def hello_world(body_param:int = Body(...)) -> str:
        return 'hello world'
```
Nota: Si en el parseo hay algún error de tipo, etc FastAPI avisa.

## Documentación
Como se comentó maneja los estándares, por esto genera documentación de OpenApi o Swagger, mediante la ruta normal más /docs.

