import unittest

from intro_biologia.el_juego_de_la_vida.desafio2 import (
    serializar_cadena_aminoacidos,
    traducir_adn_a_aminoacidos,
    validar_invariantes_adn,
    validar_invariantes_aminoacidos,
)


class TestDesafio2JuegoDeLaVida(unittest.TestCase):
    def test_validar_invariantes_adn_longitud_invalida(self):
        with self.assertRaises(ValueError):
            validar_invariantes_adn("ATGAA")

    def test_validar_invariantes_adn_alfabeto_invalido(self):
        with self.assertRaises(ValueError):
            validar_invariantes_adn("ATX")

    def test_validar_invariantes_aminoacidos_con_stop_interno(self):
        with self.assertRaises(ValueError):
            validar_invariantes_aminoacidos(["Met", "STOP", "Lys"])

    def test_traducir_adn_a_aminoacidos_ok(self):
        aminoacidos = traducir_adn_a_aminoacidos("ATGGCTAAA")
        self.assertEqual(aminoacidos, ["Met", "Ala", "Lys"])

    def test_serializar_cadena_aminoacidos(self):
        texto = serializar_cadena_aminoacidos(["Met", "Ala", "Lys"])
        self.assertEqual(texto, "Met-Ala-Lys")


if __name__ == "__main__":
    unittest.main()
