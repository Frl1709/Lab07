from database.meteo_dao import MeteoDao as m
class Model:
    def __init__(self):
        self.situation = m.get_all_situazioni()
        self.citta = m.get_citta()