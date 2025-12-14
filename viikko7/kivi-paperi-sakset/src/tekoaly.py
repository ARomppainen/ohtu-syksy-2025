from abc import ABC, abstractmethod


class Tekoaly(ABC):
    """Abstrakti pääluokka kivi, paperi ja sakset -pelin tekoälylle"""

    @abstractmethod
    def anna_siirto(self) -> str:
        """Anna seuraava siirto"""

    @abstractmethod
    def aseta_siirto(self, siirto: str) -> None:
        """Tallenna toisen pelaajan edellinen siirto muistiin"""
