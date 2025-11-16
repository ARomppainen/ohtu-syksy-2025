from parameterized import parameterized
import unittest
from unittest.mock import Mock, ANY, call
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

MAITO = Tuote(1, "maito", 5)
MEHU = Tuote(2, "mehu", 7)
PIIMA = Tuote(3, "piimä", 11)


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
            if tuote_id == MAITO.id:
                return MAITO
            if tuote_id == MEHU.id:
                return MEHU
            if tuote_id == PIIMA.id:
                return PIIMA
            return None

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.varasto_mock = varasto_mock
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

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "11111")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "11111", ANY, 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("matti", "22222")

        self.pankki_mock.tilisiirto.assert_called_with("matti", ANY, "22222", ANY, 7)

    def test_jokaiselle_maksutapahtumalle_pyydetaan_uusi_viitenumero(self):
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.side_effect = [100, 200, 300]

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "11111")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 100, ANY, ANY, ANY)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("matti", "22222")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 200, ANY, ANY, ANY)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("teppo", "33333")

        self.pankki_mock.tilisiirto.assert_called_with(ANY, 300, ANY, ANY, ANY)

    def test_poista_korista_kasvattaa_varaston_saldoa_yksi_tuote_korissa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)

        self.varasto_mock.palauta_varastoon.assert_called_once()

    def test_poista_korista_kasvattaa_varaston_saldoa_kaksi_samaa_tuotetta_korissa(
        self,
    ):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(MAITO.id)
        self.kauppa.lisaa_koriin(MAITO.id)

        # poistaa kaikki tuotteet korista, joilla id=1
        self.kauppa.poista_korista(MAITO.id)

        self.assertEqual(2, self.varasto_mock.palauta_varastoon.call_count)
        self.varasto_mock.palauta_varastoon.assert_has_calls([call(MAITO), call(MAITO)])

    def test_poista_korista_pitaa_varaston_saldon_ennallaan_jos_tuote_ei_ole_korissa(
        self,
    ):
        self.kauppa.aloita_asiointi()
        self.kauppa.poista_korista(1)

        self.varasto_mock.palauta_varastoon.assert_not_called()

    def test_poista_korista_ei_tee_mitaan_jos_tuotetta_ei_loydy(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.poista_korista(4)

        self.varasto_mock.palauta_varastoon.assert_not_called()
