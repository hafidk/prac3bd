import sqlite3 as lite
import sys

import time
from datetime import date


def llegueix_usuaris():
    """
    agafa el document dades_usuaris.txt i els volca a la bd
    """
    
    f=open("dades_usuaris.txt","r");
    c=f.readlines()
    c2=[x.strip() for x in c]
    t=[]
    for element in c2:
        t.append(tuple(element.split(" ")))
    t2=tuple(t)
    #compte amb el salt de linea al final de usuaris.txt    
    cur.executemany("INSERT INTO usuaris VALUES(?,?,?,?,?,?)", t2)
    con.commit()
    f.close()

def guarda_usuaris():
    """
    agafa tots els usuaris que tenim a la bd i els guarda al txt AL ACABAR TOT
    """
    
    cur.execute("SELECT * FROM usuaris")
    files=cur.fetchall()
    f=open("dades_usuaris.txt","w")
    for fila in files:
        f.write("%s %s %s %s %s %s" % fila +"\n")
    f.close()

def llegueix_amistats():
    """
    agafa el document dades_amistats.txt i els volca a la bd
    """
    #OJU AMB ELS PUTUS SALTS DE LINEA AL FINAL DEL FITXER TXT, EL QUART D'HORA MES EMOCIONANT DE ME VIDA
    f=open("dades_amistats.txt","r");
    c=f.readlines()
    c2=[x.strip() for x in c]
    t=[]
    for element in c2:
        t.append(tuple(element.split(" ")))
    t2=tuple(t)
    print t2
    #compte amb el salt de linea al final de usuaris.txt    
    cur.executemany("INSERT INTO amistats VALUES(?,?,?)", t2)
    #fixed... de momento
    con.commit()
    f.close()

def guarda_amistats():
    """
    agafa totes les amistats que tenim a la bd i els guarda al txt
    """
    
    cur.execute("SELECT * FROM amistats")
    files=cur.fetchall()
    f=open("dades_amistats.txt","w")
    for fila in files:
        f.write("%s %s %s" % fila +"\n")
    f.close()
    

def mostra_usuaris():
    """
    Mostra el nom i cognom de tots els usuaris que tenim
    """

    cur.execute("SELECT nom,cognom FROM usuaris")
    llista=cur.fetchall()
    for element in llista:
        print "%s %s" % element+"\n"
    return

def mostra_usuaris_personalitzat(l):
    pass

def mostra_amistats():

    cur.execute("SELECT * FROM amistats")
    llista=cur.fetchall()
    for element in llista:
        print "%s %s %s" % element+"\n"

def afegeix_usuari():
    nom=raw_input("Nom: ")
    cognom=raw_input("Cognom: ")
    email=raw_input("Email: ")
    ciutat=raw_input("ciutat: ")
    naixement=raw_input("Data: ")#format AAAA/MM/DD. m'esta donant pel cul que dona gust
    
    #anys=input("any naixement: ")
    #mes=input("mes naixement: ")
    #dia=input("dia naixement: ")
    #magia:
    #data=date(anys,mes,dia)
    #m'esta ficant nervios, no funciona
    pwd=raw_input("Pwd: ")
    packet=(email,nom,cognom,ciutat,naixement,pwd)
    print packet #el packet esta be a nivell de data
    #comanda="INSERT INTO usuaris VALUES('%s','%s','%s','%s',%s,'%s')" % packet
    cur.execute("INSERT INTO usuaris VALUES (?,?,?,?,?,?)",(email,nom,cognom,ciutat,naixement,pwd))
    return

def mostra_ciutat(city):
    """
    Mostra tots els usuaris que viuen a la ciutat tal
    """
    cur.execute("SELECT nom,cognom from usuaris WHERE poblacio = ?",(city,))
    resultat=cur.fetchall()
    for element in resultat:
        print "%s %s" % element+"\n"
    return

def mostra_edat(year):
    """
    Mostra tots els usuaris que tenen mes de x anys.
    PER FER
    """
    comanda="SELECT DataNaixament from usuaris"
    cur.execute(comanda)
    resultat=cur.fetchall()
    print resultat

def elimina_usuari(mail):
    #Parxe dolent, el execute no es menja res que no siguin tuples
    cur.execute("DELETE FROM usuaris WHERE email = ?",(mail,))
    con.commit()
    #guarda_usuaris()#perhaps fer aixo es massa d'hora
    #s'ha de afegir que si s'elimina el usuari l'amistat tambe despareix
    #vale ja se quin es el problema, a la que es carrega un usuari fa un delete d'aquella linea i tots els que estan a sota queden olvidats, depppp
    cur.execute("DELETE FROM amistats WHERE email1 = ? OR email2= ?",(mail,mail))
    #done, que bona haf, que bonnna
    #ni bona ni merdes, ara es carrega a tot sant, veamos
    return

def chng_pwd(mail,old_pwd,nw_pwd):
    cur.execute("SELECT pwd FROM usuaris WHERE email = ?",(mail,))
    resultat=cur.fetchall()
    contrasenya=resultat[0][0]
    if contrasenya==old_pwd:
        cur.execute("UPDATE usuaris SET pwd = ? WHERE email = ?",(nw_pwd,mail))
        con.commit()
    else:
        print "Antic pwd incorrecte"

def chng_poblacio(mail,nw_pb):
    cur.execute("UPDATE usuaris SET poblacio = ? WHERE email = ?",(nw_pb,mail))
    con.commit()

def envia_solicitud(mail1,mail2):
    """
    mail1 vol ser amic de mail2 (anira a pendent)
    """
    packet=(mail1,mail2,"Pendent")
    comanda="INSERT INTO amistats VALUES('%s','%s','%s')" % packet
    cur.execute(comanda)

def acepta_solicitud(mail1,mail2):
    """
    mail1 ESTEM CAIENT EN EL JOC DE QUI ACEPTA A QUI MAYDAY" acepta a mail2
    """
    #primer mirem que estigui pendent
    cur.execute("SELECT estat FROM amistats WHERE email1 = ? AND email2= ? ",(mail1,mail2))
    resultat=cur.fetchall()
    estat=resultat[0][0]

    if estat=="Pendent":
        cur.execute("UPDATE amistats SET estat='Aprovada' WHERE email1 = ? AND email2 = ?",(mail1,mail2))
        con.commit()

def rebutja_solicitud(mail1,mail2):
    """
    mail1 ESTEM CAIENT EN EL JOC DE QUI REBUTJA A QUI MAYDAY" rebutja a mail2
    """
    #primer mirem que estigui pendent

    cur.execute("SELECT estat FROM amistats WHERE email1 = ? AND email2= ? ",(mail1,mail2))
    resultat=cur.fetchall()
    estat=resultat[0][0]

    if estat=="Pendent":
        cur.execute("UPDATE amistats SET estat='Rebutjada' WHERE email1 = ? AND email2 = ?",(mail1,mail2))
        con.commit()


def amics(nom,cognom):
    """
    mostra els amics de la persona amb tal nom i cognom
    """
    cur.execute("SELECT nom,cognom FROM usuaris WHERE email in (SELECT (amistats.email2) FROM amistats, usuaris WHERE (usuaris.email=amistats.email1 AND  usuaris.nom=? and  usuaris.cognom=? and amistats.estat='Aprovada'))",(nom,cognom))
    resultat=cur.fetchall()
    for element in resultat:
        print "%s %s" % element+"\n"

def calcul_peticions(mode):
    cur.execute("SELECT count(*) from amistats where estat=?",(mode,))
    resultat = cur.fetchall()
    return resultat[0][0]

def totes_rebutjades():
    cur.execute("SELECT email1,count(email2) from amistats WHERE estat='Rebutjada' group by email1 UNION SELECT email2,count(email1) from amistats where estat='Rebutjada' group by email2")
    resultat=cur.fetchall()
    for element in resultat:
        print element[0]+ "|"+ str(element[1])
    return

def debug():
    comanda="SELECT * from amistats"
    cur.execute(comanda)
    resultat=cur.fetchall()
    for element in resultat:
        print element[0]+ "|"+ str(element[1])

def how_to():
    for i in range(5):
        print
    print """
    Benvingut/a a la xarxa social, pots utilitzar diferents opcions per tal de gestionar els diferents usuaris que tenim, el menu inicial te aquesta estructura


   |-How to
   |-afegir usuaris
   |-mostra usuaris
   |-mostra amistats
   |-acepta amistats
   |-rebutja amistats
   |-envia solicitud
   |-mes opcions d'usuaris
       |-afegir usuaris
       |-mostra amics del usuari
       |-canvia contrasenya
       |-canvia poblacio
       |-elimina l'usuari
       |-Veure total peticions (Aceptades/Rebutjades/Pendents)
       |-Veure relacio usuari/peticions rebutjades
   |-Sortir

    Afegir i mostrar usuaris/amistats son auto-explicatoris. Desde el menu principal tambe podem rebutjar amistats i enviar solicituds. En les opcions extres de administracio podem afegir usuaris a la base de dades i fer cerques de usuaris en concret(peticions,rebutjades,amistats). Tambe podem canviar informacio mes especifica com la contrasenya,poblacio,etc.
    """
    for i in range(5):
        print

con=lite.connect("prova.db")
cur=con.cursor()
cur.execute('pragma foreign_keys=ON')
cur.executescript("""
    DROP TABLE IF EXISTS usuaris;
CREATE TABLE usuaris(email varchar(20) PRIMARY KEY, nom varchar(20) NOT NULL ,cognom varchar(20),poblacio varchar(20), dataNaixament DATE, pwd varchar(20) NOT NULL); """)
#em peta al crear dominis
#on the other hand, aixo es deep shit
cur.executescript("""
   DROP TABLE IF EXISTS amistats;

   CREATE TABLE amistats(

email1 varchar(20) NOT NULL, email2 varchar(20) NOT NULL, estat varchar(10) NOT NULL, PRIMARY KEY (email1,email2), FOREIGN KEY (email1) REFERENCES usuaris(email) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (email2) REFERENCES usuaris(email) ON UPDATE CASCADE ON DELETE CASCADE); """)

con.commit()

#al inici sempre lleguirem els .txt
llegueix_usuaris()
llegueix_amistats()

while True:
    print"""
    0-How to
    1-afegir usuaris
    2-mostra usuaris
    3-mostra amistats
    4-acepta amistats
    5-rebutja amistats
    6-envia solicitud
    7-mes opcions d'usuaris
    8-sortir
    """
    op=input("Que vols fer?: ")
    print

    if op==0:
        how_to()
    
    elif op==1:
        afegeix_usuari()

    elif op==2:
        print
        print """
        1-nomes nom i cognom
        2-personalitzat
        """
        oper=input("que vols mostrar?Nomes nom i cognom o dades personalitzades")

        if oper==1:
            mostra_usuaris()
        elif oper==2:
            pass
    elif op==3:
        mostra_amistats()

    elif op==4:
        print "qui vols que sigui amic de qui"
        mostra_amistats()
        mail1=raw_input("email1: ")
        mail2=raw_input("email2: ")
        acepta_solicitud(mail1,mail2)

    elif op==5:
        print "qui vols que rebutji amistat"
        mostra_amistats()
        mail1=raw_input("email1: ")
        mail2=raw_input("email2: ")
        rebutja_solicitud(mail1,mail2)

    elif op==6:
        print "qui vols que envii amistat a qui"
        mostra_amistats()
        mail1=raw_input("email1: ")
        mail2=raw_input("email2: ")
        envia_solicitud(mail1,mail2)
    elif op==7:
        print
        print"""
        1-mostra amics del usuari
        2-canvia contrasenya
        3-canvia poblacio
        4-elimina l'usuari
        5-Veure total peticions (Aceptades/Rebutjades/Pendents)
        6-Veure relacio usuari/peticions rebutjades
        """
        while True:
            oper=input("que vols fer: ")
            
            if oper==1:
                nom=raw_input("nom usuari: ")
                cognom=raw_input("cognom usuari: ")
                amics(nom,cognom)
                
            elif oper==2:
                mail=raw_input("mail usuari: ")
                old_pwd=raw_input("contrasenya antiga")
                nw_pwd=raw_input("contrasenya nova")
                chng_pwd(mail,old_pwd,nw_pwd)
                print "contrasenya canviada"
                print
                
                #PORTO COM MITJA HORA SOLUCIONANT BUGS QUE APAREIXEN SOLS :)
            elif oper==3:
                mail=raw_input("mail usuari: ")
                nw_pb=raw_input("nova poblacio")
                chng_poblacio(mail,nw_pb)
                print "poblacio canviada"
                print 
                
            elif oper==4:
                mail=raw_input("mail del usuari a eliminar: ")
                elimina_usuari(mail)
                print "usuari eliminat"
                print
                
            elif oper==5:
                mode=raw_input("Quines vols, Aprovada/Rebutjada/Pendent: ")
                print
                print "peticions en estat %s" % mode
                print calcul_peticions(mode)
                
            elif oper==6:
                totes_rebutjades()
            
                
            else:
                break

            
    elif op==8:
        print "thats all folks!"
        guarda_usuaris()
        guarda_amistats()
        #salvados por la campana, aixo soluciona bastants problemes de concepte
        break
