class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo

    def miinus(self, operandi: int) -> None:
        self._arvo = self._arvo - operandi

    def plus(self, operandi: int) -> None:
        self._arvo = self._arvo + operandi

    def nollaa(self) -> None:
        self._arvo = 0

    def aseta_arvo(self, arvo: int) -> None:
        self._arvo = arvo

    def arvo(self) -> int:
        return self._arvo
