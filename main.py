
from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", 
	database="ispit_priprema" 
    )

from takmicar import Takmicar 


@app.route('/register', methods = ["POST","GET"])
def register():
	if request.method == "GET":
		return render_template(
			"register.html"
		)

	if request.method == "POST":
		email = request.form['email']
		sifra = request.form['sifra']
		potvrda = request.form['potvrda']
		ime_prezime = request.form['ime_prezime']
		godina_rodjenja = int( request.form['godina_rodjenja'])
		pol = request.form['pol']

		greska = Takmicar.insert(email,ime_prezime,godina_rodjenja,pol,sifra,potvrda)

		
		if greska != "":
			return render_template(
				"register.html",
				greska = greska 
			)
		
		return redirect(url_for("login"))
	
@app.route('/login',methods =["POST","GET"])
def login():
	if request.method == "GET":
		return render_template(
			"login.html"
		)
	
	if request.method == "POST":
		email = request.form['email']
		sifra = request.form['sifra']

		greska = Takmicar.login(email, sifra)
		if greska != "":
			return render_template(
				"login.html",
				greska = greska 
			)
		session['email'] = email
		
		return redirect(url_for("show_all"))
	
@app.route('/show_all')
def show_all():
	takmicari = Takmicar.dohvati_sve_takmicare()
	return render_template(
		"takmicari.html",
		takmicari = takmicari 
	)

@app.route('/delete/<email>', methods = ["POST"])
def delete(email):
	
	Takmicar.delete(email)
	return redirect(url_for("show_all"))

@app.route('/update/<email>', methods = ["POST","GET"])
def update(email):
	taj_korisnik = Takmicar.dovhati_po_email_u(email)
	if request.method == "GET":
		return render_template(
			"update.html",
			takmicar = taj_korisnik

		)
	
	if request.method == "POST":
		email = request.form['email']
		sifra = request.form['sifra']
		ime_prezime = request.form['ime_prezime']
		godina_rodjenja = int( request.form['godina_rodjenja'])
		pol = request.form['pol']

		greska = Takmicar.update(email,ime_prezime,godina_rodjenja,pol,sifra)
		if greska != "":
			return render_template(
				"update.html",
				greska = greska,
				takmicar = taj_korisnik
			)
		
@app.route('/takmicar/<email>')
def takmicar(email):
	taj_takmicar = Takmicar.dovhati_po_email_u(email)
	t1 = Takmicar.napravi_od_reda(taj_takmicar)
	return str(t1)

@app.route('/pretrazi_po_godini',methods = ["POST"])
def pretrazi_po_godini():
	if request.method== "POST":
		godina_rodjenja = request.form['godina_rodjenja']
		rez = Takmicar.pretraga_godina_rodjenja(godina_rodjenja)
		
		return render_template(
			"takmicari.html",
			takmicari = rez
		)
	
@app.route('/pretrazi_po_ime_prezime',methods = ["POST"])
def pretrazi_po_ime_prezime():
	if request.method== "POST":
		ime_prezime = request.form['ime_prezime']
		rez = Takmicar.pretraga_ime_prezime(ime_prezime)
	
		return render_template(
			"takmicari.html",
			takmicari = rez
		)
	
@app.route('/logout')
def logout():
	if "email" in session:
		session.clear()
	return redirect(url_for("login"))
app.run(debug=True)
