import uvicorn
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from starlette import status
from typing import Dict, Any

#La instancia de la app de FastAPI
app = FastAPI()

#Modificar documentación
app.title = "Aprendiendo FastAPI"
app.version = "1.0.0"


#Decorador con su atributo y en el path se puede agregar otro parametro, status_code =, es el estatus que se quiere devolver.
@app.get('/',status_code = status.HTTP_200_OK, tags = ["home"])
def hello_world() -> str:
    return 'Hello world0'
#tags=["x"] clasificación de los endpoints
@app.get('/html',tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

#Endopoint con path en la variable
@app.get('/{id}', status_code = status.HTTP_200_OK)
def chao_world(id:int = Path(ge = 1, le=2000)) -> str:
    return f'Chao {id} world'

#Endpoint con querrypath
@app.get('/prueba/', status_code = status.HTTP_200_OK)
#Los typos que se esperan en el -> son de typing
def prueba_world(param:str = Query(default = "Hola", min_length=4,max_lenght = 15), param2:int = 1) -> Dict[str, Any]:
    return {'param1': param, 'param2': param2}

#Endpoints con body
@app.post('/movies', tags=["movies"], response_model = dict,status_code = 201)
def create_movie (id: int = Body(), title: str = Body()) -> dict:
    return JSONResponse(status_code=201,content= {"message":f"Se ha registrado la pelicula {title} "})

#HTTP Response status
#Informativos 100-199
#Respuestas correctas 200-299
#200 exitosas
#201 created
#Redirecciones 300-399
#Cliente errores 400-499
#400 bad request
#401 sin autenticación
#404 no found
#Server error 500-599

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)