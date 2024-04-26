import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        self.costo_min = float('inf')
        self.sequenza_migliore = []

    def handle_umidita_media(self, e):
        situazioni = self._model.situation
        genova = []
        torino = []
        milano = []
        for s in situazioni:
            if s.data.month == self._mese:
                if s.localita == "Genova":
                    genova.append(s.umidita)
                elif s.localita == "Torino":
                    torino.append(s.umidita)
                else:
                    milano.append(s.umidita)
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text(
            f"L'umidità media nel mese selezionato è: \nGenova: {sum(genova) / len(genova):.3f} \nMilano: {sum(milano) / len(milano):.3f} \nTorino: {sum(torino) / len(torino):.3f}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        # Prendo i primi 15 giorni del mese
        tot_sit = self._model.situation
        situazioni = []
        sequenza = []
        citta = self._model.citta
        for s in tot_sit:
            if s.data.day <= 15 and s.data.month == self._mese:
                situazioni.append(s)
        self.costo_min = float('inf')
        self.ricorsione(sequenza, citta)
        tot = []
        for i in range(len(self.sequenza_migliore)):
            for ss in situazioni:
                if self.sequenza_migliore[i] == ss.localita and i+1 == ss.data.day:
                    tot.append(ss)
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(
            ft.Text(f"La sequenza ottima ha costo {self.costo_min} ed è:"))
        for element in tot:
            self._view.lst_result.controls.append(ft.Text(f"[{element.localita} - {element.data}] Umidità = {element.umidita}"))
            self._view.update_page()


    def ricorsione(self, sequenza, citta):
        # if len(sequenza) > 1:
        if len(sequenza) > 15:
            return
        if len(sequenza) < 4 and len(sequenza) > 1 and sequenza.count(sequenza[-1]) != len(sequenza):
            return
        if len(sequenza) >= 4 and sequenza[-4:-1].count(sequenza[-2]) != 3 and sequenza[-1] != sequenza[-2]:
            return
        if len(sequenza) > 1 and sequenza.count(sequenza[-1]) > 6:
            return
        if len(sequenza) == 15:
            self.calcola_costo(sequenza)
            return

        for c in citta:
            sequenza.append(c)
            self.ricorsione(sequenza, citta)
            sequenza.pop()

    def calcola_costo(self, sequenza):
        situazioni = self._model.situation
        costo = 0
        for i in range(len(sequenza)):
            for s in situazioni:
                if s.data.day == i+1 and s.localita == sequenza[i] and s.data.month == self._mese:
                    costo += s.umidita
            if i != 0 and sequenza[i-1] != sequenza[i]:
                costo += 100
        if costo <= self.costo_min:
            self.costo_min = costo
            self.sequenza_migliore.clear()
            self.sequenza_migliore.extend(sequenza)

    def read_mese(self, e):
        self._mese = int(e.control.value)
