from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #enkripcija za cookie i sesije
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #pokreće bazu sa flask app

    from .views import views #importovanje pregleda u app
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') #registrovanje blueprintova sa prefiksom /
    app.register_blueprint(auth, url_prefix='/')
    #da piše u zagradi 'auth/' , morali bismo napraviti rutu u auth fajlu npr @auth.route("test")
    from .models import Korisnik #impotuje se tabela, da bi se učitala pre instanciranja tabele
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #gde login menager mora ići ako se zahteva user
    login_manager.init_app(app)

    @login_manager.user_loader #ovaj dekorator se koristi za pronalazenje usera
    def load_user(id): #uzima ID i govori flasku kako uzimamo usera, ne mora se napomenuti 'GET'
        #po defaultu traži primarni key
        return Korisnik.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME): #ako ne postoji, pravi se nova tabela
        db.create_all(app=app)
        print('Created Database!')
