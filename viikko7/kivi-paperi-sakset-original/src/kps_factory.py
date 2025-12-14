from enum import Enum

from kps import KiviPaperiSakset
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_pelaaja_vs_tekoaly import KPSPelaajaVsTekoaly
from tekoaly_parannettu import TekoalyParannettu
from tekoaly_vuorotteleva import TekoalyVuorotteleva


class Pelityyppi(Enum):
    """Pelityyppi kivi, paperi ja sakset -pelille"""

    PELAAJA_VS_PELAAJA = 1
    PELAAJA_VS_TEKOALY = 2
    PELAAJA_VS_PAREMPI_TEKOALY = 3


def luo_kps_peli(pelityyppi: Pelityyppi) -> KiviPaperiSakset:
    """Luo uusi kivi, paperi ja sakset -peli"""
    match pelityyppi:
        case Pelityyppi.PELAAJA_VS_PELAAJA:
            return KPSPelaajaVsPelaaja(input_func=input, print_func=print)
        case Pelityyppi.PELAAJA_VS_TEKOALY:
            return KPSPelaajaVsTekoaly(
                TekoalyVuorotteleva(), input_func=input, print_func=print
            )
        case Pelityyppi.PELAAJA_VS_PAREMPI_TEKOALY:
            return KPSPelaajaVsTekoaly(
                TekoalyParannettu(10), input_func=input, print_func=print
            )
