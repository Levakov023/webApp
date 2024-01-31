from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import SudskaOdluka, Sud
from . import db
from .servisi import DodajSudServis, DodajSudskuOdlukuServis, AzuriranjeServis
import json
from flask import flash
from .PoslovnaLogika import PoslovnaLogika, LogikaJMBG

config_path = 'website/config.json'
with open('website/config.json', 'r') as file_config:
    config = json.load(file_config)

max_jmbg = config.get("maksimalan_broj_jmbgova") # OVO JE ZA POSLOVNU LOGIKU I IMPORT CONFIGA

azuriranje_servis = AzuriranjeServis()
dodaj_sud_service = DodajSudServis()
dodaj_odluku_service = DodajSudskuOdlukuServis()
ValidacijaJMBG = LogikaJMBG()
#blueprint za izdvajanje pregleda u više fajlova
views = Blueprint('views', __name__)
#definisanje blueprinta



@views.route('/stampa-azuriranje/<int:odlukaID>', methods=['GET', 'POST'])
@login_required
def stampa_azuriranje(odlukaID):

    return redirect(url_for('views.home'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        jmbg_filter = request.form.get('jmbg_filter')
        if jmbg_filter:
            # Filtrirajte sudske odluke na osnovu unetog filtera
            sudske_odluke = SudskaOdluka.query.filter(SudskaOdluka.JMBG_list.contains(jmbg_filter)).all()
        else:
            # Ako filter nije unet, prikažite sve sudske odluke
            sudske_odluke = SudskaOdluka.query.all()
    else:
        # Ako nije poslat POST zahtev, prikažite sve sudske odluke
        sudske_odluke = SudskaOdluka.query.all()

    return render_template("glavno.html", user=current_user, sudski_odluke=sudske_odluke)

@views.route('dodajOdluku', methods = ['GET', 'POST'])
@login_required
def dodaj():
    sudovi = Sud.query.all()

    if request.method == 'POST':
        naslov = request.form.get('naslov')
        sadrzaj = request.form.get('sadrzaj')
        jmbg_list_str = request.form.get('jmbg_list')
        sud_ime = request.form.get('sud')
        if ValidacijaJMBG.validacija(jmbg_list_str):
            if dodaj_odluku_service.dodaj(naslov, sadrzaj, jmbg_list_str, sud_ime):
                flash('Нова одлука је додата!', category='success')
            else:
                flash('Суд са изабраним именом није пронађен или није могуће додати одлуку.', category='error')
    return render_template("dodajOdluku.html", user=current_user, sudovi=sudovi)

@views.route('/dodajSud', methods=['GET', 'POST'])
@login_required
def dodaj_sud():
    if request.method == 'POST':
        naziv = request.form.get('naziv')
        mesto = request.form.get('mesto')

        # Koristite servis za dodavanje suda
        if dodaj_sud_service.dodaj(naziv, mesto):
            flash('Суд је успешно додат!', category='success')
            return redirect(url_for('views.home'))  # Redirektuj korisnika na glavnu stranicu nakon dodavanja suda
        else:
            flash('Морате унети све информације.', category='error')

    return render_template("dodajSud.html", user=current_user)

@views.route('/stampa-odluke/<int:odlukaID>', methods=['GET'])
def stampa_odluke(odlukaID):
    odluka = SudskaOdluka.query.get(odlukaID)
    if not odluka:
        flash('Sudska odluka nije pronađena.', category='error')
        return redirect(url_for('views.home'))

    # Dodajte odluku suda u odluku
    sud = Sud.query.get(odluka.sud_id)
    if sud:
        odluka.sud = sud

    return render_template("stampa.html", user=current_user, odluka=odluka)

@views.route('/delete-odluka/<int:odluka_id>', methods=['POST','GET'])
def delete_odluka(odluka_id):
    odluka = SudskaOdluka.query.get(odluka_id)
    db.session.delete(odluka)
    db.session.commit()
    flash('Одлука је успешно обрисана!', category='success')
    return redirect(url_for('views.home'))

@views.route('/azuriranje/<int:odlukaID>', methods=['GET', 'POST'])
@login_required
def azuriranje(odlukaID):
    odluka = SudskaOdluka.query.get(odlukaID)
    sudovi = Sud.query.all()  # Dohvatite sve sudove za padajući izbornik

    if not odluka:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        naslov = request.form.get('naslov')
        sadrzaj = request.form.get('sadrzaj')
        sud_id = request.form.get('sud_id')
        jmbg_list_str = request.form.get('jmbg_list')

        if azuriranje_servis.dodaj(odluka, naslov, sadrzaj, jmbg_list_str, sud_id):
            flash('Одлука је успешно ажурирана!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Морате унети све информације.', category='error')

    return render_template("azuriranje.html", user=current_user, odluka=odluka, sudovi=sudovi)


