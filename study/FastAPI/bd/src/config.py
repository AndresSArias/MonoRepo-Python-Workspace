from sqlmodel import (
    #Crear motor de comunicación
    create_engine, 
    #Genera las clases/tablas o objetos en py para futuramente la bd
    SQLModel, Field, 
    #Mediante el moto, una sesión es para generar operaciones en la bd
    Session,
    #Operaciones
    select,
    #En el where -> or, columna especial 
    or_,col
)

#Nombre de la bd 
sqlite_file_name = "database.db"
#url de la conexión
sqlite_url = f"sqlite:///{sqlite_file_name}"
#Crear el motor que mantendra la conexión, parametrso de url y echo para mostrar sentencias ejecutadas.
engine = create_engine(sqlite_url, echo=False)

#Clase que mediante la herencia de SQLModel y parametro table, generará una tabla en la bd
class Hero(SQLModel, table=True):
    #Valor opcional, porque en el defecto que no lo envié, se generará una id automaticamente y se ceclara que es primary_key..
    id: int | None = Field(default=None, primary_key=True)
    #Valores requeridos, serán No Null con su respetivo tipo
    name: str 
        #Creamos un índice en la columna secret_name, optimizan la busqueda, requiere más espacio en la bd y tiempo de escritura.
        #recomendado si es un valor que constantemente sale en los wheres.
    secret_name: str = Field(index=True)  
    #Valor opcional, lo que marcará en la bd Null
    age: int | None = None
    team_id: int | None = Field(default=None, foreign_key="team.id")

    def __str__ (crs):
        return f'Todos me conocen por {crs.secret_name}, pero en realidad soy {crs.name} y tengo {crs.age} años con id de {crs.id} y pertenezco al equipo {crs.team_id}'
    
#Una segunda clase/tabla para referenciar en la primera
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    def __str__ (crs):
        return f'Este es el equipo {crs.name} con headquarters {crs.headquarters} y id {crs.id}'

# python -> bd
# int -> INTEGER
# str -> VARCHAR


#Operación en memoria de crear registos, objetos de las tablas.
def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age = 95)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)   
    hero_8 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_9 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_10 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)     

    #Uso with para cerrar la session después de usarla, usa el motor de comunicación
    with Session(engine) as session:
        #.add en la sesión agrega un registro en la trabla corespondiente al modelo        
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        
        #.add_all adjunta una lista de la misma tabla/una lista de instancias de la misma clase
        session.add_all([hero_8, hero_9, hero_10, hero_4, hero_5, hero_6, hero_7])

        #guarda todo los cambios en un solo paso
        session.commit()

        #Refrescar manualmente los datos de un registro desde la base de datos hacía el objeto en python.
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

def create_teams():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

def create_heroes_with_relation():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")  # Sin equipo
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        # Refrescar y mostrar los héroes
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def select_heroes():
    with Session(engine) as session:

        #querry a querer ejecutar
        statement = select(Hero)

        #objeto iterable de sqlalchemy, "ScalarResult"
        #results = session.exec(statement)

                
        #List[x] de x clase/tabla
        results = session.exec(statement).all()


        print(f'soy de tipo {type(results)}')
        for hero in results:
            print(hero)


def select_heroes_where():
    with Session(engine) as session:

        print("selecc cuando el heroe sea Deadpod")
        statement = select(Hero).where(Hero.name == "Deadpond")

        results = session.exec(statement)
        for hero in results:
            print(hero)

        print("selecc cuando el heroe tengas más de 35 años")
        statement = select(Hero).where(Hero.age > 35)
        results = session.exec(statement)
        for hero in results:
            print(hero)            

        print("selecc cuando héroes con una edad entre 35 y 39 años.")
        # Usando múltiples .where()
        #statement = select(Hero).where(Hero.age >= 35).where(Hero.age < 40)

        # Pasando múltiples condiciones a .where()
        statement = select(Hero).where(Hero.age >= 35, Hero.age < 40)
        results = session.exec(statement)
        for hero in results:
            print(hero)          

        print("Esta consulta seleccionará héroes con edad menor o igual a 35, o mayor a 90.")
        statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90))
        results = session.exec(statement)
        for hero in results:
            print(hero)     

        print("Esta consulta seleccionará héroes con edad mayor o igual a 35, teniendo presente la columna especial age que es Null (puede ser null en la bd o None acá en la bd)")
        statement = select(Hero).where(col(Hero.age) >= 35)
        results = session.exec(statement)
        for hero in results:
            print(hero)     

def selec_heroes_one_row():
    with Session(engine) as session:
        print("El primer heroe encontrado es")
        statement = select(Hero).where(Hero.age <= 96)
        results = session.exec(statement)
        #Retorna la primera fila encontrada o None si no hay
        hero = results.first()
        print("Hero:", hero)

        print("El único heroe encontrado es:")
        statement = select(Hero).where(Hero.name == "asd")
        results = session.exec(statement)
        try:
            #Retorna la única fila encontrada y lanza error si hay cero o más de una.
            hero = results.one()
            print("Hero:", hero)             
        except Exception as nrf:
            print(f'tipo: {nrf} y soy {nrf}')
            print('hay cero o más de una registros')
        
        id = 10
        print(f'El heroe con la pk {id}')
        #Busca directamente por clave primaria (por ejemplo, id). Si no encuentra, retorna None.
        hero = session.get(Hero, id)  # Busca el héroe con id=1
        print("Hero:", hero)

def selec_heroes_range_row():
    with Session(engine) as session:
        #en la creación del querry, .limit(#) número max de rangos devueltos. con -1 trae a todos.
        elemetos = 3
        pagina = 5
        print('3 elementos')
        statement = select(Hero).limit(elemetos)
        results = session.exec(statement)
        heroes = results.all()
        for hero in heroes:
            print(hero) 
        #.offset(x), pasa la x página con # de elementos por .limit(#)
        print('página 5 con 3 elementos')
        statement = select(Hero).where(Hero.age > 32).offset(pagina).limit(elemetos)
        results = session.exec(statement)
        heroes = results.all()
        for hero in heroes:
            print(hero) 

def update_heroe():
    with Session(engine) as session:
        hero = session.get(Hero,10)
        print(f'antes de actualizar\n{hero}')
        hero.age = 99
        session.commit()

        hero = session.get(Hero,10)
        print(f'antes de actualizar\n{hero}')
        

def delete_heroe():
    with Session(engine) as session:
        hero = session.get(Hero,10)

        session.delete(hero)

        session.commit()


def select_join_heroes():
    with Session(engine) as session:
        #Trae sólo a los hereos con equipos.
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)    
        
        #Join left, incluye a todos los que tiene la fk, así no tenga.
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)       
        #Cuando se quiere sólo seleccionar el heroe con respecto a una relación fk. 
        statement = select(Hero).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        for hero in results:
            print("Preventer Hero:", hero)        

def create_db_and_tables():
    #Método que ejecuta la creación de todas las tablas, parametro el motor de comunicación.
    SQLModel.metadata.create_all(engine)
    
