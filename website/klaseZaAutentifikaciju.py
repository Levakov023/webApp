from abc import ABC, abstractmethod
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash
from flask_login import login_user
from .models import db, Korisnik


class AutentifikacijaServis(ABC):
    @abstractmethod
    def izvrsi_prijavu(self, *args, **kwargs):
        pass

    @abstractmethod
    def izvrsi_registraciju(self, *args, **kwargs):
        pass


class DefaultAutentifikacijaServis(AutentifikacijaServis):
    def izvrsi_prijavu(self, email, sifra):
        korisnik = Korisnik.query.filter_by(email=email).first()

        if korisnik:
            if check_password_hash(korisnik.sifra, sifra):
                flash('Uspešno ste se prijavili!', category='success')
                login_user(korisnik, remember=True)
                return True
            else:
                flash('Netačna šifra.', category='error')
        else:
            flash('Email adresa ne postoji.', category='error')

        return False

    def izvrsi_registraciju(self, email, ime, sifra1, sifra2, jeovlascen):
        korisnik = Korisnik.query.filter_by(email=email).first()

        if korisnik:
            flash('Email adresa već postoji.', category='error')
        elif len(email) < 4:
            flash('Email adresa mora biti duža od 3 karaktera.', category='error')
        elif len(ime) < 2:
            flash('Ime mora sadržati bar 2 slova.', category='error')
        elif sifra1 != sifra2:
            flash('Unete šifre se ne poklapaju.', category='error')
        elif len(sifra1) < 7:
            flash('Šifra mora sadržati bar 7 karaktera.', category='error')
        else:
            novi_korisnik = Korisnik(email=email, ime=ime, sifra=generate_password_hash(sifra1, method='sha256'),
                                     jeovlascen=jeovlascen)
            db.session.add(novi_korisnik)
            db.session.commit()
            login_user(novi_korisnik, remember=True)
            flash('Uspešno ste kreirali nalog!', category='success')
            return True

        return False