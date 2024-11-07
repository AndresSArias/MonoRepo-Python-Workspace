import uvicorn
from fastapi import (
    FastAPI, 
    Depends, 
    Header,
    HTTPException,
    Request,
)
from pydantic import BaseModel
from typing import List
from time import time
app = FastAPI()

#Serializador con campos obligatorios
class User (BaseModel):
    id: int
    name: str
    def __str__(crs):
        return f'Hola soy {crs.name} y me id es {crs.id}'
    
#"Relaciones" entre serializadores
class School (BaseModel):
    students: List[User]

    def __str__(crs):
# Crear una lista de mensajes para cada estudiante y luego unirlos en una cadena
        return "\n".join(
            f"Hola soy {student.name} y mi id es {student.id}"
            for student in crs.students
        )

school = School(students=[])

@app.post('/student',response_model = School, status_code = 201)
def create_student(student:User) -> School:
    school.students.append(student)
    return school

#Depends como captador de querry params
def get_name (name:str ) -> str:
    return name

@app.get('/student', response_model = List[User])
def list_students (name_for_shear: str = Depends(get_name)):
    return[student for student in school.students if name_for_shear in student.name]

#Depends como filtro desde los querry, con una clase y modificando su forma de equals.
class StudentFilter:
    def __init__(self, age:int = 0, name:str = Depends(get_name)) :
        self.age = age
        self.name = name
    def __eq__(self, other: 'StudentFilter') -> bool:
        return self.age == other.age or self.name == other.name
    
@app.get('/studentsbyage', response_model = List[User])
def get_students_by_age_or_name (student_filter: StudentFilter = Depends(StudentFilter)):
    return[student for student in school.students if student_filter == StudentFilter(name=student.name)]  

#Depends en el path, validadores
def validate_token(x_token: str = Header(...)):
    if x_token != 'Bearer':
        raise HTTPException(status_code = 401, detail = 'Token Invalido')
    
@app.get('/hola', dependencies = [Depends(validate_token)])
def get_hola(txt:str)-> str:
    return f'Hola {txt} pasaste'

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time()-start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

if __name__ == '__main__':
    uvicorn.run(app='main:app',reload=True)