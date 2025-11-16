from tuote import Tuote


class Ostoskori:
    def __init__(self):
        self._tuotteet: list[Tuote] = []

    def lisaa(self, tuote: Tuote):
        self._tuotteet.append(tuote)

    def poista(self, tuote: Tuote) -> int:
        ennen = len(self._tuotteet)
        self._tuotteet = list(filter(lambda t: t.id != tuote.id, self._tuotteet))
        jalkeen = len(self._tuotteet)
        return ennen - jalkeen

    def hinta(self):
        hinnat = map(lambda t: t.hinta, self._tuotteet)

        return sum(hinnat)
