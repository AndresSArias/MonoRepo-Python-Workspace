# Pydantic
Es una libreria de validación y serialización de la información, basada en la libreria [typing](https://docs.python.org/3/library/typing.html#module-typing), que son los tipos del propio de Python que se le deben agregar a las diferentes variables y propiedad, sobre párametros que espera. Así valida la información de sus modelos de manera Dinamica.

## Modelo base en pydantic
```python

    from typing import List, Optional
    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        friends: List[int]
    
    User(id = '1', friends = [2,3])
    #Transforma el 1 str a int por la validació dinámica.

```

## En endpoints de FastAPI
La integración es muy sencilla, ya que FastAPI se desarrolló con este objetivo de crear serializadores con Pydantic, así.

```python
    class Person (BaseModel):
        age: int
        name: str
    @app.post('/person', response_model = Person)
    def creat_person (person: Person) -> Person:
        return person

```

con el atributo response_model el endpoint es capaz de validar toda la información que entra y sale con el modelo de Pydantic, en el caso de la entrada de un endpoint post, directamente revisa el payload del body con el modelo de pydantic.

## Ventajas de usar pydantic
* Serialización sencilla
* Validación automatica.
* Usa el typing nativo de python
* Genera autimáticamente la documentación


