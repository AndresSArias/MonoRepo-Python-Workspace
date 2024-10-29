import uvicorn
from fastapi import FastAPI
from starlette import status
from typing import Dict, Any

#La instancia de la app de FastAPI
app = FastAPI()

#Decorador con su atributo y en el path se puede agregar otro parametro, status_code =, es el estatus que se quiere devolver.
@app.get('/',status_code = status.HTTP_200_OK)
def hello_world() -> str:
    return 'Hello world0'

#Endopoint con path en la variable
@app.get('/{id}', status_code = status.HTTP_200_OK)
def chao_world(id:int) -> str:
    return f'Chao {id} world'

#Endpoint con querrypath
@app.get('/prueba/', status_code = status.HTTP_200_OK)
#Los typos que se esperan en el -> son de typing
def prueba_world(param:str = 'Hola', param2:int = 1) -> Dict[str, Any]:
    return {'param1': param, 'param2': param2}

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)