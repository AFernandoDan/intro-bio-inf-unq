import unittest

from intro_biologia.desafio5 import ChouFasmanPredictor, predict_secondary_structure


class TestChouFasmanPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = ChouFasmanPredictor()

    def test_predice_helix_sin_conflicto(self):
        sequence = ["A", "E", "L", "M", "Q", "K"]
        result = self.predictor.predict(sequence)
        self.assertEqual(result.secondary_structure, "HHHHHH")

    def test_predice_strand_sin_conflicto(self):
        sequence = ["V", "I", "Y", "C", "F"]
        result = self.predictor.predict(sequence)
        self.assertEqual(result.secondary_structure, "BBBBB")

    def test_resuelve_conflicto_por_promedio(self):
        sequence = ["L", "M", "F", "W", "I", "T"]
        result = self.predictor.predict(sequence)
        self.assertEqual(result.secondary_structure, "BBBBBH")

    def test_normaliza_minusculas(self):
        sequence = ["a", "e", "l", "m", "q", "k"]
        structure = predict_secondary_structure(sequence)
        self.assertEqual(structure, "HHHHHH")

    def test_simbolo_invalido_levanta_error(self):
        with self.assertRaises(ValueError):
            self.predictor.predict(["A", "X", "L"])


if __name__ == "__main__":
    unittest.main()
