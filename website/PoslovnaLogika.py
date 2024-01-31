import json
from abc import ABC, abstractmethod
from flask import flash
config_path = 'website/config.json'

class PoslovnaLogika(ABC):

    @abstractmethod
    def ucitajConfig(self, *args, **kwargs):
        pass

    @abstractmethod
    def validacija(self, *args, **kwargs):
        pass


class LogikaJMBG(PoslovnaLogika):
    def __init__(self):
        self.config_fajl = self.ucitajConfig()

    def ucitajConfig(self):
        with open(config_path, 'r') as file_config:
            config = json.load(file_config)
        return config

    def validacija(self, jmbg_unos):
        jmbg_lista  = [jmbg.strip() for jmbg in jmbg_unos.split(',') if jmbg.strip()]
        max_jmbg = self.config_fajl.get('maksimalan_broj_jmbgova')
        if len(jmbg_lista) > max_jmbg:
            flash('Прекорачили сте максималан број ЈМБГ-ова!', category='error')
            return False
        return True

class poslovnaLogika:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        config = json.load(config_file)


        pass

        def validacija_jmbg(self, sudski_postupak):
            max_jmbg = self.config.get('maksimalan_broj_jmbgova')
            jmbg_lista = len(sudski_postupak.jmbg_list)
            if jmbg_lista > max_jmbg :
                return False
            else :
                return True

