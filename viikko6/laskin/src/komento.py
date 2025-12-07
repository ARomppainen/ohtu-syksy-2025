from abc import ABC
from typing import Callable

from sovelluslogiikka import Sovelluslogiikka


class AKomento(ABC):
    def __init__(self, pino: list["AKomento"], logiikka: Sovelluslogiikka):
        self._pino = pino
        self._logiikka = logiikka
        self._aikaisempi_tila = logiikka.arvo()

    def suorita(self) -> None: ...

    def kumoa(self) -> None:
        self._logiikka.aseta_arvo(self._aikaisempi_tila)


class Summa(AKomento):
    def __init__(
        self,
        pino: list[AKomento],
        logiikka: Sovelluslogiikka,
        lue_syote: Callable[[], int | None],
    ):
        super().__init__(pino, logiikka)
        self._lue_syote = lue_syote

    def suorita(self) -> None:
        if (syote := self._lue_syote()) is not None:
            self._logiikka.plus(syote)
            self._pino.append(self)


class Erotus(AKomento):
    def __init__(
        self,
        pino: list[AKomento],
        logiikka: Sovelluslogiikka,
        lue_syote: Callable[[], int | None],
    ):
        super().__init__(pino, logiikka)
        self._lue_syote = lue_syote

    def suorita(self) -> None:
        if (syote := self._lue_syote()) is not None:
            self._logiikka.miinus(syote)
            self._pino.append(self)


class Nollaus(AKomento):
    def __init__(self, pino: list[AKomento], logiikka: Sovelluslogiikka):
        super().__init__(pino, logiikka)

    def suorita(self) -> None:
        self._logiikka.nollaa()
        self._pino.append(self)


class Kumoa(AKomento):
    def __init__(self, pino: list[AKomento], logiikka: Sovelluslogiikka):
        super().__init__(pino, logiikka)

    def suorita(self) -> None:
        if len(self._pino) > 0:
            self._pino.pop().kumoa()
