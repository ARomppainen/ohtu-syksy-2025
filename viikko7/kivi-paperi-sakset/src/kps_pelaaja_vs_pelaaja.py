from kps import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):

    def _toisen_siirto(self, ensimmaisen_siirto):
        return self._input("Toisen pelaajan siirto: ")
