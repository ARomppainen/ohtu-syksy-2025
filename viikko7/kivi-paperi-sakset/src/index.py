from kps_factory import Pelityyppi, luo_kps_peli


def _valitse_pelityyppi() -> Pelityyppi | None:
    print(
        "Valitse pelataanko"
        "\n (a) Ihmistä vastaan"
        "\n (b) Tekoälyä vastaan"
        "\n (c) Parannettua tekoälyä vastaan"
        "\nMuilla valinnoilla lopetetaan"
    )

    vastaus = input()
    match (None if len(vastaus) == 0 else vastaus[-1]):
        case "a":
            return Pelityyppi.PELAAJA_VS_PELAAJA
        case "b":
            return Pelityyppi.PELAAJA_VS_TEKOALY
        case "c":
            return Pelityyppi.PELAAJA_VS_PAREMPI_TEKOALY
        case _:
            return None


def main():
    while (pelityyppi := _valitse_pelityyppi()) is not None:
        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )
        peli = luo_kps_peli(pelityyppi)
        peli.pelaa()


if __name__ == "__main__":
    main()
