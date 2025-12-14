from abc import ABC, abstractmethod
from typing import Callable

from tuomari import Tuomari

KIVI = "k"
PAPERI = "p"
SAKSET = "s"

type InputFunc = Callable[[str], str]
type PrintFunc = Callable[[str], None]


class KiviPaperiSakset(ABC):
    """
    Abstrakti pääluokka kivi, paperi ja sakset -pelille,
    missä pelaaja #1 on aina ihmispelaaja.
    """

    def __init__(self, input_func: InputFunc, print_func: PrintFunc):
        self._input = input_func
        self._print = print_func

    def pelaa(self) -> None:
        """Pelaa kivi, paperi ja sakset -peliä"""
        tuomari = Tuomari()

        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            self._print(str(tuomari))

            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)

        self._print("Kiitos!")
        self._print(str(tuomari))

    def _ensimmaisen_siirto(self) -> str:
        return self._input("Ensimmäisen pelaajan siirto: ")

    @abstractmethod
    def _toisen_siirto(self, ensimmaisen_siirto) -> str: ...

    def _onko_ok_siirto(self, siirto: str):
        return siirto in (KIVI, PAPERI, SAKSET)
