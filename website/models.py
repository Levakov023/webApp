from . import db #from package, da smo van foldera bilo bi from website
from flask_login import UserMixin #klasa za nasledjivanje za flask login
from sqlalchemy.sql import func # uzima trenutno vreme i datum , func.now()



class Korisnik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    sifra = db.Column(db.String(150))
    ime = db.Column(db.String(150))
    jeovlascen = db.Column(db.Boolean, default=False)

class Sud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False) # nullable = ne sme biti prazno
    mesto = db.Column(db.String(255), nullable=False)


class SudskaOdluka(db.Model):
    OdlukaID = db.Column(db.Integer, primary_key=True)
    Naslov = db.Column(db.String(255), nullable=False)
    Sadrzaj = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    JMBG_list = db.Column(db.JSON, nullable=False)
    sud_id = db.Column(db.Integer, db.ForeignKey('sud.id'), nullable=False)
    sud = db.relationship('Sud', backref='odluke')


    """
class Advokat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(255), nullable=False)"""


"""class Predmet(db.Model):
    PredmetID = db.Column(db.Integer, primary_key=True)
    Naslov = db.Column(db.String(255), nullable=False)
    Sadrzaj = db.Column(db.Text, nullable=False)
    datum = db.Column(db.DateTime(timezone=True), default=func.now())
    JMBG_list = db.Column(db.JSON, nullable=False)
    advokat_id = db.Column(db.Integer, db.ForeignKey('advokat.id'), nullable=False)
    advokat = db.relationship('Advokat', backref='predmeti')
"""