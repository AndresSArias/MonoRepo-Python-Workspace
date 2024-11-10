import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.tile= "API con autenticación"
app.version = "1.0.0"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "a@a.com":
            return HTTPException(status_code=403, detail="Credenciales no son validas")
        
class User(BaseModel):
    email:str
    password: str

@app.post('/login',tags=['auth'],response_model=str,status_code=200)
def login(user:User) -> str:
    if user.email == "a@a.com" and user.password == "123":
        token: str = create_token(user.dict())
        return JSONResponse (status_code = 200, content =token)
    else:
        return user.email == "a@a.com" and user.password == "123"

@app.get('/hola',tags=['home'], response_model = str, status_code = 200, dependencies=[Depends(JWTBearer())])
def hola ()->str:
    return JSONResponse(status_code= 200, content = "HolA")

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)