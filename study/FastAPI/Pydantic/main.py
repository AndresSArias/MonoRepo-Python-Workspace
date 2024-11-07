import uvicorn

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from fastapi import FastAPI

app = FastAPI()

#Serializador con campos obligatorios
class User (BaseModel):
    id: int
    name: str
    def __str__(crs):
        return f'Hola soy {crs.name} y me id es {crs.id}'
class UserSinRequeridos(BaseModel):
    id: int
    # Si se coloca un = (valor por defecto cuando se envía None, toma ese valor)
    name: str = 'Juan'
    #Usando Optional, no es necesario colocar un valor por defecto porque se vuelve requerido, sin embargo se puede 
    # dejar un valor None en el envío del parametro
     
    last_name: Optional[str]

    def __str__(crs):
        return f'Hola soy {crs.name} y me id es {crs.id}, dijo {crs.last_name}'    

#"Relaciones" entre serializadores
class School (BaseModel):
    students: List[User]

    def __str__(crs):
# Crear una lista de mensajes para cada estudiante y luego unirlos en una cadena
        return "\n".join(
            f"Hola soy {student.name} y mi id es {student.id}"
            for student in crs.students
        )

class UserConRestricciones (BaseModel):
    id: int
    name: Optional[str]
    #gt = greater than (mayor que) 
    #lt = less than (menor que)
    # ... = Es requerido, si colocas un valor será el de defecto y si no colocas saldrá error.
    age: int = Field (...,gt = 0, lt =18)
    weight: int

    @field_validator('weight')
    def weight_is_not_greater_than(cls, weight: int) -> int:
        if weight > 100:
            raise ValueError('User es muy pesado')
        return weight +1

    def __str__(crs):
        return f'Hola soy {crs.name} y me id es {crs.id} con una edad de {crs.age} con peso {crs.weight}'    

school = School(students=[])

@app.post('/student',response_model = School, status_code = 201)
def create_student(student:User) -> School:
    school.students.append(student)
    return school


if __name__ == '__main__':
    user = User (id=0,name="1")
    user1 = UserSinRequeridos(id = 1,last_name = None)
    
    students = [User(id=i,name=f"student {i}") for i in range(10)]
    
    escuela = School(students = students)
    
    user2 = UserConRestricciones(id=1,name="Sapo",age =15,weight= 15)
    
    json_to_user = User.parse_obj({'id':10,'name':'hola'})
    
    json_to_user2 = User(**{'id':10,'name':'hola'})    
    
    
    print(json_to_user2)
    
    print (user.schema_json())
    #print (escuela)
    
    #print(user1)



    uvicorn.run(app='main:app',reload=True)
