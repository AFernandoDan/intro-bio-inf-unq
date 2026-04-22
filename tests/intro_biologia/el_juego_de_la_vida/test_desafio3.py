import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from intro_biologia.el_juego_de_la_vida.desafio3 import (
    ejecutar_cli,
    identificar_regiones_promotoras,
    leer_secuencia_desde_archivo,
)


class TestDesafio3JuegoDeLaVida(unittest.TestCase):
    def test_identificar_region_promotora_caso_ideal(self):
        secuencia = "CGATCGTATAAAGGGCCCATCTATAAAGTC"
        regiones = identificar_regiones_promotoras(secuencia)

        self.assertEqual(len(regiones), 1)
        self.assertEqual(regiones[0]["secuencia"], "TATAAAGGGCCCATCTATAAA")
        self.assertEqual(regiones[0]["inicio"], 6)
        self.assertEqual(regiones[0]["fin"], 26)

    def test_identificar_region_promotora_caso_incompleto(self):
        secuencia = "AGCTAGTATAAACCCGGGTTTAAA"
        regiones = identificar_regiones_promotoras(secuencia)
        self.assertEqual(regiones, [])

    def test_identificar_region_promotora_caso_multiple(self):
        secuencia = "CGATATAAACCCTATAAAGGGTATAAAT"
        regiones = identificar_regiones_promotoras(secuencia)

        self.assertEqual(len(regiones), 2)
        self.assertEqual(regiones[0]["secuencia"], "TATAAACCCTATAAA")
        self.assertEqual(regiones[1]["secuencia"], "TATAAAGGGTATAAA")

    def test_leer_secuencia_desde_archivo_fasta(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo = Path(tmpdir) / "entrada.fasta"
            archivo.write_text(">id1\nCGATATAAACCCTATAAAGGGTATAAAT\n", encoding="utf-8")

            secuencia = leer_secuencia_desde_archivo(str(archivo))
            self.assertEqual(secuencia, "CGATATAAACCCTATAAAGGGTATAAAT")

    def test_cli_caso_multiple(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo = Path(tmpdir) / "entrada.fasta"
            archivo.write_text(">id1\nCGATATAAACCCTATAAAGGGTATAAAT\n", encoding="utf-8")

            salida = io.StringIO()
            with redirect_stdout(salida):
                codigo = ejecutar_cli([str(archivo)])

            self.assertEqual(codigo, 0)
            texto = salida.getvalue()
            self.assertIn("Se encontraron 2 region(es) promotora(s):", texto)
            self.assertIn("TATAAACCCTATAAA", texto)
            self.assertIn("TATAAAGGGTATAAA", texto)


if __name__ == "__main__":
    unittest.main()
