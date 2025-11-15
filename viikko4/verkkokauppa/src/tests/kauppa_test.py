from parameterized import parameterized
import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 20
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "mehu", 7)
            if tuote_id == 3:
                return Tuote(3, "piimä", 11)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.pankki_mock = pankki_mock
        self.kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    @parameterized.expand(
        [
            ("yksi tuote", [1], "pekka", "11111", 5),
            ("kaksi eri tuotetta", [1, 2], "matti", "22222", 12),
            ("kaksi samaa tuotetta", [2, 2], "teppo", "33333", 14),
            ("toinen tuotteista loppu", [2, 3], "paavo", "44444", 7),
        ]
    )
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikein(
        self, _, ostokset: list[int], nimi: str, tili_numero: str, summa: int
    ):
        self.kauppa.aloita_asiointi()
        for tuote_id in ostokset:
            self.kauppa.lisaa_koriin(tuote_id)
        self.kauppa.tilimaksu(nimi, tili_numero)

        self.pankki_mock.tilisiirto.assert_called_with(
            nimi, ANY, tili_numero, ANY, summa
        )
