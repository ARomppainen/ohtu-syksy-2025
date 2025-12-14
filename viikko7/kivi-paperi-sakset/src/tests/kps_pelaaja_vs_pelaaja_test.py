from unittest import TestCase
from unittest.mock import Mock
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja


class TestKPSPelaajaVsPelaaja(TestCase):
    def test_pelaa(self):
        siirrot = ["k", "p", "k", "k", "k", "s", "", ""]

        mock_input = Mock(side_effect=siirrot)
        mock_print = Mock()

        peli = KPSPelaajaVsPelaaja(input_func=mock_input, print_func=mock_print)
        peli.pelaa()

        self.assertEqual(8, mock_input.call_count)

        for i in (0, 2, 4, 6):
            self.assertEqual(
                "Ensimmäisen pelaajan siirto: ", mock_input.call_args_list[i][0][0]
            )
        for i in (1, 3, 5, 7):
            self.assertEqual(
                "Toisen pelaajan siirto: ", mock_input.call_args_list[1][0][0]
            )

        self.assertEqual(5, mock_print.call_count)

        self.assertEqual(
            "Pelitilanne: 0 - 1\nTasapelit: 0",
            mock_print.call_args_list[0][0][0],
        )
        self.assertEqual(
            "Pelitilanne: 0 - 1\nTasapelit: 1",
            mock_print.call_args_list[1][0][0],
        )
        self.assertEqual(
            "Pelitilanne: 1 - 1\nTasapelit: 1",
            mock_print.call_args_list[2][0][0],
        )
        self.assertEqual("Kiitos!", mock_print.call_args_list[3][0][0])
        self.assertEqual(
            "Pelitilanne: 1 - 1\nTasapelit: 1",
            mock_print.call_args_list[4][0][0],
        )
