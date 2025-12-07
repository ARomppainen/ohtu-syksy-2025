from abc import ABC
from typing import Callable

from sovelluslogiikka import Sovelluslogiikka


class AKomento(ABC):
    def suorita(self) -> None: ...


class Summa(AKomento):
    def __init__(self, logiikka: Sovelluslogiikka, lue_syote: Callable[[], int | None]):
        self._logiikka = logiikka
        self._lue_syote = lue_syote

    def suorita(self) -> None:
        if (syote := self._lue_syote()) is not None:
            self._logiikka.plus(syote)


class Erotus(AKomento):
    def __init__(self, logiikka: Sovelluslogiikka, lue_syote: Callable[[], int | None]):
        self._logiikka = logiikka
        self._lue_syote = lue_syote

    def suorita(self) -> None:
        if (syote := self._lue_syote()) is not None:
            self._logiikka.miinus(syote)


class Nollaus(AKomento):
    def __init__(self, logiikka: Sovelluslogiikka):
        self._logiikka = logiikka

    def suorita(self) -> None:
        self._logiikka.nollaa()


class Kumoa(AKomento):
    def __init__(self, logiikka: Sovelluslogiikka):
        self._logiikka = logiikka

    def suorita(self) -> None:
        pass
