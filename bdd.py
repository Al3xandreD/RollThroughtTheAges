import sqlite3 as sqt

def connection():
    try:
        con = sqt.connect("RTTA.db")    # connexion
    except sqt.DatabaseError as er:
        print("There is a problem with the connection to the database", er)
    else:
        try:
            cursor = con.cursor()  # création du curseur
        except sqt.DatabaseError as er:
            print("Failed to create the cursor", er)
    return cursor, con

def create_tables(cursor, con):
    cursor.execute("create table  if not exists matches ("
                   "num_m number(5) PRIMARY KEY NOT NULL, " # id du match
                   "winner number(5), "     # gagnants de la partie
                   "looser number(5),"  # perdants de la partie
                   "f_score number(3),"     # score finale de la partie
                   "date_part date)")   # date de la partie

    cursor.execute("create table if not exists player("
                   "num_p number(5) PRIMARY KEY NOT NULL, "   # id du joueur
                   "nom_p char(10), "    # nom du player
                   "nb_m_p number(5),"   # nombre de partie jouée "
                   "nb_m_w number(5))")  # nombre de partie gagnée "

    cursor.execute("create table if not exists construction("
                   "c_nm char(10) PRIMARY KEY NOT NULL,"  # construction's name
                   "c_owner number(5))")  # construction's owner

    # valeurs=(2, "le Alex", 50, 0)
    # cursor.execute(f'insert into player values {valeurs}')
    # con.commit()


# manipulation de la BDD
def insertion_match(cursor, table, valeurs):
    '''Allows the insertion of a tuple in a table using
    a cursor'''

    cursor.execute('insert into ' + table + ' values ' + valeurs)
    cursor.commit()

def insertion_player(cursor, table, valeurs,num_player):
    '''Allows the insertion of a tuple in a table using
    a cursor'''

    cursor.execute('insert into ' + table + ' values ' + valeurs+' where '+str(num_player)+'=nump_p')
    cursor.commit()

def fetch_player(cursor, table, iD,nb_rows=0 ,all=False,):
    '''Allows the fetching of a table's rows,
     all rows or nb_rows number of rows'''

    if all == True:
        cursor.execute('select * from ' + table + ' where '+str(iD)+'=num_p')
        rows = cursor.fetchall()
    else:
        cursor.execute('select * from ' + table)
        rows = cursor.fetchmany(nb_rows)
    return rows

def mx_giD(cursor):
    '''Return the biggest number used for the gameiD,
    used to generate one for a new player'''

    res = cursor.execute('select max(num_p) from player')
    rep = res.fetchone()
    return rep
