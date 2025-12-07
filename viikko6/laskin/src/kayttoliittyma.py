from enum import Enum
from tkinter import Tk, ttk, constants, StringVar
from typing import Callable
from komento import AKomento, Summa, Erotus, Nollaus, Kumoa
from sovelluslogiikka import Sovelluslogiikka


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka: Sovelluslogiikka, root: Tk):
        self._logiikka = sovelluslogiikka
        self._root = root
        self._pino: list[AKomento] = []
        self._komentotehdas: dict[Komento, Callable[[], AKomento]] = {
            Komento.SUMMA: lambda: Summa(self._pino, self._logiikka, self._lue_syote),
            Komento.EROTUS: lambda: Erotus(self._pino, self._logiikka, self._lue_syote),
            Komento.NOLLAUS: lambda: Nollaus(self._pino, self._logiikka),
            Komento.KUMOA: lambda: Kumoa(self._pino, self._logiikka),
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._logiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA),
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS),
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS),
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA),
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        try:
            return int(self._syote_kentta.get())
        except ValueError:
            return None

    def _suorita_komento(self, komento: Komento) -> None:
        komento_olio = self._komentotehdas[komento]()
        komento_olio.suorita()

        self._kumoa_painike["state"] = (
            constants.DISABLED if len(self._pino) == 0 else constants.NORMAL
        )

        self._nollaus_painike["state"] = (
            constants.DISABLED if self._logiikka.arvo() == 0 else constants.NORMAL
        )

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._logiikka.arvo())
