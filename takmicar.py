import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", 
	database="ispit_priprema" 
    )

class Takmicar:
    id : int
    email : str 
    ime_prezime : str 
    godina_rodjenja : int 
    pol : str 
    sifra : str 
    def __init__(self, id,email, ime_prezime,godina_rodjenja,pol,sifra) -> None:
        self.id = id 
        self.email = email
        self.ime_prezime = ime_prezime
        self.godina_rodjenja = godina_rodjenja
        self.pol = pol 
        self.sifra = sifra

    @classmethod
    def napravi_od_reda(cls, red):
        taj_takmicar = red
        
        return cls(taj_takmicar[0],taj_takmicar[1],taj_takmicar[2],taj_takmicar[3],taj_takmicar[4],taj_takmicar[5])
    
    def __str__(self) -> str:
        return f"""
            <p> ID: {self.id} </p> \n
            <p> Email: {self.email} </p> \n
            <p> Ime i prezime: {self.ime_prezime} </p> \n
            <p> Godina rodjenja: {self.godina_rodjenja} </p> \n
            <p> Pol: {self.pol} </p> \n
            <p> Sifra: {self.sifra} </p> \n
        """
    @staticmethod
    def dekodiraj_tapl(tapl):
        tapl = list(tapl) 
        n = len(tapl)
        for i in range(n):
            if isinstance(tapl[i],bytearray): 
                tapl[i] = tapl[i].decode() 
        return tapl 
    
    @staticmethod
    def dekodiraj_listu_taplova(lista_taplova):
        n = len(lista_taplova)
        for i in range(n):
            lista_taplova[i] = Takmicar.dekodiraj_tapl(lista_taplova[i])
        return lista_taplova


    @staticmethod
    def dovhati_po_id_u(id):
        cursor = mydb.cursor(prepared=True)
        sql = f"SELECT * FROM takmicari WHERE id = ?"
        parametri = (id,) 
        cursor.execute(sql, parametri)
        rez = cursor.fetchone() 
        if rez != None:
            rez = Takmicar.dekodiraj_tapl(rez)
        return rez 
    
    @staticmethod
    def dovhati_po_email_u(email):
        cursor = mydb.cursor(prepared=True)
        sql = f"SELECT * FROM takmicari WHERE email = ?"
        parametri = (email,) 
        cursor.execute(sql, parametri)
        rez = cursor.fetchone() 
        if rez != None:
            rez = Takmicar.dekodiraj_tapl(rez)
        return rez 
    
    @staticmethod
    def dohvati_sve_takmicare():
        cursor = mydb.cursor(prepared=True)
        sql = "SELECT * FROM takmicari"
        cursor.execute(sql)
        rez = cursor.fetchall() 
        rez = Takmicar.dekodiraj_listu_taplova(rez)
        return rez 
    
    @staticmethod
    def validiraj_email(email):
        if Takmicar.dovhati_po_email_u(email) != None:
            return "Takmicar sa tim emailom vec postoji"
        if "@" not in email:
            return "Ne postoji oznaka @ u emailu"
        return ""
    
    @staticmethod
    def validiraj_godina_rodjenja(godina_rodjenja):
        if godina_rodjenja < 1900:
            return "Godina rodjenja ne moze da bude manja od 1900"
        return ""
    
    @staticmethod
    def validiraj_ime_prezime(ime_prezime):
        if len(ime_prezime) < 3:
            return "Duzina imena i prezimena mora da bude makar 3 karaktera"
        return ""
    
    @staticmethod
    def validiraj_pol(pol):
        if pol not in ["Muski","Zenski"]:
            return "Pol nije odgovarajuci"
        return ""

    @staticmethod
    def insert(email, ime_prezime,godina_rodjenja,pol, sifra,potvrda):
        greska = Takmicar.validiraj_email(email) 
        greska += Takmicar.validiraj_godina_rodjenja(godina_rodjenja)
        greska += Takmicar.validiraj_ime_prezime(ime_prezime)
        greska += Takmicar.validiraj_pol(pol)
        if potvrda != sifra:
            greska += "Sifre se razlikuju!"
        if greska == "":
            cursor = mydb.cursor(prepared=True)
            sql = f"INSERT INTO takmicari VALUES(null, ?,?,?,?,?)"
            parametri = (email,ime_prezime,godina_rodjenja,pol,sifra)
            
            cursor.execute(sql,parametri)
            mydb.commit()
            return "" 
        else:
            return greska
        
    @staticmethod
    def delete(email):
        cursor = mydb.cursor(prepared=True)
        sql = "DELETE FROM takmicari WHERE email = ?"
        paramteri = (email,)
        cursor.execute(sql,paramteri)
        mydb.commit()
        return "Uspesno brisanje"
    
    @staticmethod
    def update(email,ime_prezime,godina_rodjenja,pol,sifra):
        
        greska = Takmicar.validiraj_godina_rodjenja(godina_rodjenja)
        greska += Takmicar.validiraj_ime_prezime(ime_prezime)
        greska += Takmicar.validiraj_pol(pol)
        nas_takmicar = Takmicar.dovhati_po_email_u(email)
        
        if sifra != nas_takmicar[5]:
            greska += "Sifre se razlikuju"

        if greska == "":
            cursor = mydb.cursor(prepared=True)
            sql = f"""
                UPDATE takmicari
                SET email = ?,
                ime_prezime = ?,
                godina_rodjenja = ?,
                pol = ?
                WHERE email = ?
            
            """
            parametri = (email,ime_prezime,godina_rodjenja,pol,email)
            print(sql)
            cursor.execute(sql,parametri)
            mydb.commit()
            return "Uspesno proslo"
        else:
            return str(greska)
        
    
    @staticmethod
    def login(email, password):
        rez = Takmicar.dovhati_po_email_u(email)
        greska = "" 
        if rez == None:
           return "Takmicar sa tim emailom ne postoji"
        
        if greska == "" and password != rez[5]: 
            return "Sifre se ne poklapaju"
        
        return greska
    
    @staticmethod
    def pretraga_godina_rodjenja(godina_rodjenja):
        cursor = mydb.cursor(prepared=True)
        sql = "select * from takmicari where godina_rodjenja = ?"
        parametri = ( godina_rodjenja,)
        cursor.execute(sql, parametri)
        rez = cursor.fetchall()
        rez = Takmicar.dekodiraj_listu_taplova(rez)
        return rez 
    
    @staticmethod
    def pretraga_ime_prezime(ime_prezime):
        cursor = mydb.cursor(prepared=True)
    
        sql = "select * from takmicari where ime_prezime LIKE ?"
        parametri = ( f"%{ime_prezime}%",)
        cursor.execute(sql, parametri)
        rez = cursor.fetchall()
        rez = Takmicar.dekodiraj_listu_taplova(rez)
        return rez 

        
    



    


        