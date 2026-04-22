import unittest

from intro_biologia import Aminoacido, Proteina
from intro_biologia.desafio5 import (
    ChouFasmanPredictor,
    PrediccionEstructuraSecundaria,
    TipoEstructuraSecundaria,
    parsear_secuencia_texto,
    parse_proteina_desde_texto,
    predecir_estructura_secundaria,
)


class TestChouFasmanPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = ChouFasmanPredictor()

    def test_predice_helix_sin_conflicto(self):
        sequence = ["A", "E", "L", "M", "Q", "K"]
        result = self.predictor.predecir(sequence)
        self.assertEqual(result.secondary_structure_string, "HHHHHH")
        self.assertTrue(all(isinstance(aa, Aminoacido) for aa in result.sequence))
        self.assertIsInstance(result, PrediccionEstructuraSecundaria)

    def test_predice_strand_sin_conflicto(self):
        sequence = ["V", "I", "Y", "C", "F"]
        result = self.predictor.predecir(sequence)
        self.assertEqual(result.secondary_structure_string, "BBBBB")

    def test_resuelve_conflicto_por_promedio(self):
        sequence = ["L", "M", "F", "W", "I", "T"]
        result = self.predictor.predecir(sequence)
        self.assertEqual(result.secondary_structure_string, "BBBBBH")

    def test_normaliza_minusculas(self):
        sequence = ["a", "e", "l", "m", "q", "k"]
        structure_es = predecir_estructura_secundaria(sequence)
        self.assertEqual(structure_es, "HHHHHH")

    def test_simbolo_invalido_levanta_error(self):
        with self.assertRaises(ValueError):
            self.predictor.predecir(["A", "X", "L"])

    def test_predice_desde_proteina(self):
        proteina = Proteina("Demo", [
            Aminoacido.alanina(),
            Aminoacido.acido_glutamico(),
            Aminoacido.leucina(),
            Aminoacido.metionina(),
            Aminoacido.glutamina(),
            Aminoacido.lisina(),
        ])
        result = self.predictor.predecir_estructura_secundaria_de_proteina(proteina)
        self.assertEqual(result.secondary_structure_string, "HHHHHH")
        self.assertEqual(result.secondary_structure[0], TipoEstructuraSecundaria.HELICE)

    def test_parse_sequence_text_soporta_fasta(self):
        text = ">seq1\naelmqk\n"
        sequence_es = parsear_secuencia_texto(text)
        self.assertEqual([aa.simbolo for aa in sequence_es], ["A", "E", "L", "M", "Q", "K"])

    def test_parse_proteina_desde_texto(self):
        proteina = parse_proteina_desde_texto("P1", "VIYCF")
        self.assertEqual(proteina.nombre, "P1")
        self.assertEqual([aa.simbolo for aa in proteina.secuencia], ["V", "I", "Y", "C", "F"])

    def test_representaciones_textuales(self):
        proteina = Proteina("P2", [Aminoacido.alanina(), Aminoacido.valina()])
        self.assertEqual(repr(proteina), "Proteina(P2, n=2, secuencia='AV')")

        resultado = self.predictor.predecir(["A", "E", "L", "M", "Q", "K"])
        texto = repr(resultado)
        self.assertIn("PrediccionEstructuraSecundaria", texto)
        self.assertIn("estructura='HHHHHH'", texto)


if __name__ == "__main__":
    unittest.main()
