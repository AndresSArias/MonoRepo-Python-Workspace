from src.config import create_db_and_tables, create_heroes, create_teams, create_heroes_with_relation, delete_heroe, selec_heroes_one_row, selec_heroes_range_row,select_heroes, select_heroes_where, select_join_heroes, update_heroe

if __name__ == "__main__":
    create_db_and_tables()
    #create_heroes()
    #create_teams()
    #select_heroes()
    #select_heroes_where()
    #selec_heroes_one_row()
    #selec_heroes_range_row()
    #update_heroe()
    #delete_heroe()

    #create_heroes_with_relation()
    select_join_heroes()