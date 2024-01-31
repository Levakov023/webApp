from abc import ABC, abstractmethod
from .models import db, Sud, SudskaOdluka

class DodajServis(ABC):
    @abstractmethod
    def dodaj(self, *args, **kwargs):
        pass


class DodajSudServis(DodajServis):
    def dodaj(self, naziv, mesto):
        if not naziv or not mesto:
            return False

        novi_sud = Sud(naziv=naziv, mesto=mesto)
        db.session.add(novi_sud)
        db.session.commit()
        return True

class DodajSudskuOdlukuServis(DodajServis):
    def dodaj(self, naslov, sadrzaj, jmbg_list_str, sud_ime):
        sud = Sud.query.filter_by(naziv=sud_ime).first()

        if sud:
            jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
            nova_odluka = SudskaOdluka(Naslov=naslov, Sadrzaj=sadrzaj, JMBG_list=jmbg_list, sud=sud)
            db.session.add(nova_odluka)
            db.session.commit()
            return True
        else:
            return False


class AzuriranjeServis(DodajServis):
    def dodaj(self, odluka, naslov, sadrzaj, jmbg_list_str, sud_id):
        if not naslov or not sadrzaj or not jmbg_list_str or not sud_id:
            return False

        odluka.Naslov = naslov
        odluka.Sadrzaj = sadrzaj
        odluka.sud_id = sud_id

        jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
        odluka.JMBG_list = jmbg_list

        db.session.commit()
        return True


"""from abc import ABC, abstractmethod
from .models import db, Advokat, Predmet

class DodajServis(ABC):
    @abstractmethod
    def dodaj(self, *args, **kwargs):
        pass

class DodajAdvokatServis(DodajServis):
    def dodaj(self, naziv, mesto):
        if not naziv or not mesto:
            return False

        novi_advokat = Advokat(naziv=naziv, mesto=mesto)
        db.session.add(novi_advokat)
        db.session.commit()
        return True

class DodajPredmetServis(DodajServis):
    def dodaj(self, naslov, sadrzaj, jmbg_list_str, advokat_ime):
        advokat = Advokat.query.filter_by(naziv=advokat_ime).first()

        if advokat:
            jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
            novi_predmet = Predmet(Naslov=naslov, Sadrzaj=sadrzaj, JMBG_list=jmbg_list, advokat=advokat)
            db.session.add(novi_predmet)
            db.session.commit()
            return True
        else:
            return False

class AzuriranjeServis(DodajServis):
    def dodaj(self, predmet, naslov, sadrzaj, jmbg_list_str, advokat_id):
        if not naslov or not sadrzaj or not jmbg_list_str or not advokat_id:
            return False

        predmet.Naslov = naslov
        predmet.Sadrzaj = sadrzaj
        predmet.advokat_id = advokat_id

        jmbg_list = [jmbg.strip() for jmbg in jmbg_list_str.split(',') if jmbg.strip()]
        predmet.JMBG_list = jmbg_list

        db.session.commit()
        return True"""