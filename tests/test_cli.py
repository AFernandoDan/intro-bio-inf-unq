import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from intro_biologia.cli import ejecutar_cli


class TestCliPrediccion(unittest.TestCase):
    def test_cli_con_secuencia_directa_texto(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = ejecutar_cli(["--secuencia", "AELMQK", "--id", "p1"])

        self.assertEqual(codigo, 0)
        texto = salida.getvalue()
        self.assertIn("ID: p1", texto)
        self.assertIn("Secuencia:  AELMQK", texto)
        self.assertIn("Estructura: HHHHHH", texto)

    def test_cli_con_fasta_y_salida_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo_entrada = Path(tmpdir) / "entrada.fasta"
            archivo_entrada.write_text(">prot1\nAELMQK\n>prot2\nVIYCF\n", encoding="utf-8")

            salida = io.StringIO()
            with redirect_stdout(salida):
                codigo = ejecutar_cli(["--input", str(archivo_entrada), "--formato", "json"])

            self.assertEqual(codigo, 0)
            payload = json.loads(salida.getvalue())
            self.assertEqual(len(payload), 2)
            self.assertEqual(payload[0]["id"], "prot1")
            self.assertEqual(payload[0]["estructura_secundaria"], "HHHHHH")
            self.assertEqual(payload[1]["id"], "prot2")
            self.assertEqual(payload[1]["estructura_secundaria"], "BBBBB")

    def test_cli_escribe_archivo_tsv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo_salida = Path(tmpdir) / "salida.tsv"
            codigo = ejecutar_cli([
                "--secuencia",
                "VIYCF",
                "--id",
                "p2",
                "--formato",
                "tsv",
                "--output",
                str(archivo_salida),
            ])

            self.assertEqual(codigo, 0)
            contenido = archivo_salida.read_text(encoding="utf-8")
            self.assertTrue(contenido.startswith("id\tposicion\tresiduo\testructura"))
            self.assertIn("p2\t1\tV\tB", contenido)

    def test_cli_error_por_fuentes_multiples(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                ejecutar_cli(["--secuencia", "AELMQK", "--stdin"])

    def test_cli_error_archivo_inexistente(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            codigo = ejecutar_cli(["--input", "tres_proteinas.fasta"])

        self.assertEqual(codigo, 2)
        self.assertIn("No existe el archivo de entrada", stderr.getvalue())

    def test_cli_error_salida_invalida(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            salida_invalida = Path(tmpdir) / "carpeta" / "salida.tsv"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                codigo = ejecutar_cli([
                    "--secuencia",
                    "AELMQK",
                    "--output",
                    str(salida_invalida),
                ])

            self.assertEqual(codigo, 2)
            self.assertIn("Error de sistema de archivos", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
