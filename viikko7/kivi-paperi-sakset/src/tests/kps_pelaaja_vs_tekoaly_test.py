from unittest import TestCase
from unittest.mock import Mock
from kps_pelaaja_vs_tekoaly import KPSPelaajaVsTekoaly
from tekoaly import Tekoaly


class TestKPSPelaajaVsPelaaja(TestCase):
    def test_pelaa(self):
        siirrot = ["k", "p", "s", ""]

        mock_input = Mock(side_effect=siirrot)
        mock_print = Mock()

        mock_tekoaly = Mock(spec=Tekoaly)
        mock_tekoaly.anna_siirto.return_value = "k"

        peli = KPSPelaajaVsTekoaly(
            mock_tekoaly, input_func=mock_input, print_func=mock_print
        )
        peli.pelaa()

        self.assertEqual(4, mock_input.call_count)

        for i in range(4):
            self.assertEqual(
                "Ensimmäisen pelaajan siirto: ", mock_input.call_args_list[i][0][0]
            )

        self.assertEqual(9, mock_print.call_count)

        for i in (0, 2, 4, 6):
            self.assertEqual("Tietokone valitsi: k", mock_print.call_args_list[i][0][0])

        self.assertEqual(
            "Pelitilanne: 0 - 0\nTasapelit: 1",
            mock_print.call_args_list[1][0][0],
        )
        self.assertEqual(
            "Pelitilanne: 1 - 0\nTasapelit: 1",
            mock_print.call_args_list[3][0][0],
        )
        self.assertEqual(
            "Pelitilanne: 1 - 1\nTasapelit: 1",
            mock_print.call_args_list[5][0][0],
        )
        self.assertEqual("Kiitos!", mock_print.call_args_list[7][0][0])
        self.assertEqual(
            "Pelitilanne: 1 - 1\nTasapelit: 1",
            mock_print.call_args_list[8][0][0],
        )
