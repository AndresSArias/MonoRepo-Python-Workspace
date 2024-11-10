## BASES DE DATOS CON SQLMODEL
Una base de datos (DB) es un sistema estructurado y eficiente para almacenar y gestionar datos mediante tablas interconectadas. SQLModel trabaja específicamente con bases de datos relacionales. Una base de datos permite almacenar datos de forma persistente, garantizando su integridad y facilitando el acceso eficiente, algo que se vuelve esencial para cualquier aplicación.

### Tipos de bases de datos
#### Base de datos como archivo único
Ejemplo, SQLite. Aquí, la base de datos se gestiona dentro de un archivo.
#### Servidor de bases de datos
Por ejemplo, PostgreSQL o MySQL. Estas bases de datos funcionan como aplicaciones en un servidor y permiten conexiones remotas.
#### Servidores distribuidos
Para bases de datos que necesitan manejar grandes volúmenes de datos y redundancia, una base de datos distribuida en varios servidores permite balancear la carga.

### Bases de datos SQL vs NoSQL
SQLModel se enfoca en bases de datos SQL (relacionales), las cuales estructuran los datos en tablas con relaciones bien definidas entre ellas. Las bases de datos NoSQL, por otro lado, pueden almacenar datos de diferentes maneras (almacenamiento de documentos, de grafos, clave-valor, etc.), pero no son el enfoque de SQLModel.

### Tablas y relaciones en SQL
* Tablas: Los datos se organizan en filas y columnas. Cada fila representa un registro y cada columna, un atributo de los registros.
* Llaves primarias: Cada fila tiene una clave primaria única para identificar el registro en la tabla.
* Llaves foráneas y relaciones: Las llaves foráneas permiten que una tabla referencie registros de otra tabla, estableciendo así relaciones entre datos, lo que es esencial en bases de datos relacionales.

### SQL - El lenguaje
SQL (Structured Query Language) es el lenguaje usado para interactuar con bases de datos relacionales. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre los datos, además de la creación y modificación de tablas y otros elementos de la base de datos.

### SQLModel para trabajar con SQL
SQLModel facilita escribir código en Python para manipular bases de datos SQL de manera más natural. Se basa en SQLAlchemy y Pydantic, lo que le permite definir modelos con validación de datos y convertir automáticamente estos modelos en sentencias SQL.

#### ORM y SQL
Así se crea una tabla mediante una clase en python con SQLModel
```python
    class Hero(SQLModel):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None
```
Tener  presente que se pueden crear statment (querrys de sql) y ejecutarlas, así.

```python

    user_id = input("Type the user ID: ")

    statement = f"SELECT * FROM hero WHERE id = {user_id};"

    results = database.execute(statement)
```
Pero lo anterior puede tener injection sql si user_id es "2; DROP TABLE hero", para esto SQLModel propone la siguiente solución:

```python
    user_id = input("Type the user ID: ")

    session.exec(
        select(Hero).where(Hero.id == user_id)
    ).all()
```

Porque sí la entrada es como la enmarcada en comillas, el querry a ejecutar sería "SELECT * FROM hero WHERE id = "2; DROP TABLE hero;";".

#### Select con where.
La siguiente sentencia
```sql
    SELECT * FROM hero WHERE secret_identity = 'Dive Wilson';
```
Se consigue en SQLModel así.
````python
    database.execute(
        select(Hero).where(Hero.secret_name == "Dive Wilson")
    ).all()

```

### Limitación de SQLModel a SQL Databases
Aunque SQLModel es poderoso para bases de datos SQL, no ofrece soporte directo para bases de datos NoSQL. Sin embargo, al ser SQL Databases ampliamente utilizadas y con capacidades de relaciones, suelen cubrir las necesidades de muchos proyectos.