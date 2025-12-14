from kps import KiviPaperiSakset, InputFunc, PrintFunc
from tekoaly import Tekoaly


class KPSPelaajaVsTekoaly(KiviPaperiSakset):
    def __init__(self, tekoaly: Tekoaly, input_func: InputFunc, print_func: PrintFunc):
        super().__init__(input_func, print_func)
        self._tekoaly = tekoaly

    def _toisen_siirto(self, ensimmaisen_siirto):
        siirto = self._tekoaly.anna_siirto()
        self._print(f"Tietokone valitsi: {siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return siirto
