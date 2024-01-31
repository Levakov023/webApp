from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Korisnik
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .klaseZaAutentifikaciju import DefaultAutentifikacijaServis

autentifikacija_servis = DefaultAutentifikacijaServis()
auth = Blueprint('auth', __name__)
#pregledni blueprint 'auth'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        sifra = request.form.get('sifra')

        if autentifikacija_servis.izvrsi_prijavu(email, sifra):
            return redirect(url_for('views.home'))

    return render_template("login.html", user=current_user)


@auth.route('/logout') #ruta za logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if request.method == 'POST':
        email = request.form.get('email')
        ime = request.form.get('ime')
        sifra1 = request.form.get('sifra1')
        sifra2 = request.form.get('sifra2')
        jeovlascen = request.form.get('jeovlascen') == 'on'

        if autentifikacija_servis.izvrsi_registraciju(email, ime, sifra1, sifra2, jeovlascen):
            return redirect(url_for('views.home'))

    return render_template("registracija.html", user=current_user)