from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None  ## ==  id: int | None = None
    #max_lenght, maximo de tamaño de un str
    #min_lenght, mínimo del tamaño del str
    #default, valor por defecto en la documentación para ejemplo y/o generar petición.
    title: str = Field(default = "mi peli",max_lenght =15, min_lenght = 5)
    overview:str
    #gt = greater than (mayor que) 
    #ge = greater equals (menor o igual)
    #lt = less than (menor que)
    #le = less equals (menor o igual)
    year:int = Field(default= 2022,le = 2022, )
    rating:float
    category:str

    model_config = {
        "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "title": "Mi Pelicula",
                        "overview": "Descripcion de la pelicula",
                        "year": 2022,
                        "rating": 9.9,
                        "category": "Acción"
                    }
                ]
            }
        }
    

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("This email is already registered")
        return value
