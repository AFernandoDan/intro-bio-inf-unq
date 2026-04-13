import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

from intro_biologia.desafio7 import (
    crear_regex_desde_motivo,
    descargar_fasta_uniprot,
    ejecutar_cli,
    buscar_motivo_en_secuencia,
)


class TestDesafio7(unittest.TestCase):
    def test_crear_regex_desde_motivo_y_coincidencias_solapadas(self):
        regex = crear_regex_desde_motivo("ABA")
        self.assertEqual(regex.pattern, "(?=(ABA))")

        coincidencias = buscar_motivo_en_secuencia(regex, "ABABA")
        self.assertEqual(coincidencias, [(1, "ABA"), (3, "ABA")])

    def test_cli_con_fasta_y_motivo_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo_entrada = Path(tmpdir) / "entrada.fasta"
            archivo_entrada.write_text(">prot1\nABABA\n", encoding="utf-8")

            salida = io.StringIO()
            with redirect_stdout(salida):
                codigo = ejecutar_cli([
                    "--input",
                    str(archivo_entrada),
                    "--motivo",
                    "ABA",
                    "--formato",
                    "json",
                ])

            self.assertEqual(codigo, 0)
            payload = json.loads(salida.getvalue())
            self.assertEqual(payload[0]["id"], "prot1")
            self.assertEqual(payload[0]["coincidencias"], [
                {"posicion": 1, "texto": "ABA"},
                {"posicion": 3, "texto": "ABA"},
            ])

    def test_cli_texto_recorta_secuencia_larga(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo_entrada = Path(tmpdir) / "entrada.fasta"
            archivo_entrada.write_text(">prot1\nAAAAAAAAAABBBBBBBBBBCCCCCCCCCCDDDDDDDDDD\n", encoding="utf-8")

            salida = io.StringIO()
            with redirect_stdout(salida):
                codigo = ejecutar_cli([
                    "--input",
                    str(archivo_entrada),
                    "--motivo",
                    "AAAA",
                    "--formato",
                    "texto",
                ])

            self.assertEqual(codigo, 0)
            texto = salida.getvalue()
            self.assertIn("Secuencia: AAAAAAAAAA...DDDDDDDDDD", texto)
            self.assertIn("Coincidencias:", texto)

    @patch("intro_biologia.desafio7.urllib.request.urlopen")
    def test_descargar_fasta_uniprot_y_buscar_motivo(self, mock_urlopen):
        contenido_fasta = b">sp|P12345|TEST_HUMAN Test protein\nABABA\n"
        respuesta = MagicMock()
        respuesta.status = 200
        respuesta.read.return_value = contenido_fasta
        mock_urlopen.return_value.__enter__.return_value = respuesta

        texto = descargar_fasta_uniprot("P12345")
        self.assertIn(">sp|P12345|TEST_HUMAN Test protein", texto)

        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = ejecutar_cli([
                "--ids",
                "P12345",
                "--motivo",
                "ABA",
                "--formato",
                "texto",
            ])

        self.assertEqual(codigo, 0)
        self.assertIn("ID: sp|P12345|TEST_HUMAN Test protein", salida.getvalue())
        self.assertIn("Posicion 1", salida.getvalue())

    def test_cli_error_sin_motivo(self):
        salida = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(salida):
                ejecutar_cli(["--input", "entrada.fasta"])


if __name__ == "__main__":
    unittest.main()
