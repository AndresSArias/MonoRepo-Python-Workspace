# Dependencias
Son atributos, parametros o funciones que necesita un endpoint para funcionar correctamente. Para funcionar FastAPI usa Depends(), donde ejecutará primero lo de andetro antes de ejecutar el endpoint, así se ve.

```python

    @app.get('/user')
    def list_users(db: DB=Depends(get_db)) -> List[User]:
        return db.get_users()

```
Esto funciona por el inyector de independencias, que compone un árbol jerarquico que contiene las dependencias que necesita cada uno de los endpoints y hasta subdependecias.

## Depends con querry params
FastAPI, permite añadir valores de la request directamente en el depends, así. 
```python

    def common_parameters (q:Optional[str] = None, limit : int = 100):
        return {'q':q,'limit':limit}

    @app.get('/items0')
    def read_items(commons:dict = Depends(common_parameters)):
        return commons


```
Si en varios endpoints recoge los mismos queryparams, el depends podría recopilar toda la info.

## Depends como validador / Depends en el path
Las dependencias dentro de un endpoint, siempre deben devolver un valor para el endpoint, aún así cuando se usa en un decorador, o sea dependencias del path, no tienen que devolver un valor, y en caso que lo haga, lo ignorará. Ya que se usan para validar,se ejecutan mucho antes de entrar al endpoint. Por ejemplo que un token tenga un valor correspondiente, que la request es correcta, normalmente ejecutan raise después de comprobaciones como las anteriores.
```python

    def verify_token(x_key:str = Header(...)):
        if x_key == ""
        raise InbalidHeader()
    @app.get("/items", dependencias = [Depends(verify_token)])
    def read_items():
        return {}

```
En los Depends, también se pueden inyectar componentes de FastAPI, cómo son Header(), Body(), entre otros. FastAPI adapta en el caso de Header, toda la nomenclatura por guión de un header, x-key, a lower case como es x_key, también automatiza el caso de camel case xKey a lowe case x_key.

## Dependencias como generadores.
Son valores que devuelve el Depends en el yield, ejecuta el endpoint y al final del endpoint regresan para terminar de ejecutar el Depends, esto sirve para cerrar la conexión de las db.

```python

    def get_db():
        create_connection()
        yield connection
        remove_connection()
    
    @app.get("/items")
    def read_users (db:DB =) Depends(get_db):
        return db.get_users()
```
### Ventajas
* Compartir lógica entre componentes
* Abstracción de componentes externos
* Simplifica el trabajo con FastAPI y sus componentes, querryparams, Hears, Body
* Muy fácul crear authenticadores
* Documentación automática.

### Depends vs Middlewares
Como vimos antes las dependencias son muy útiles y versatiles, aún así una middleware es un componente por el cual todas las request y response pasan por ella. Sólo se pueden adjuntar al nivel de aplicación con el decorador así.

```python
    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start_time = time()
        reponse = await call_next(request)
        process_time = time()-start_time
        reponse.headers['X-Process-Time'] = str(process_time)
        return response

```
Modifican el contenido de todas la reques y la response.