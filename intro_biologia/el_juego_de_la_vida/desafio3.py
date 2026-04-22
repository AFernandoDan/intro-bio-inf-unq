from __future__ import annotations

import argparse
from pathlib import Path


MOTIVO_TATA = "TATAAA"


def leer_secuencia_desde_archivo(ruta_archivo: str) -> str:
	"""Lee una secuencia de ADN desde un archivo de texto o FASTA."""
	contenido = Path(ruta_archivo).read_text(encoding="utf-8").replace("\ufeff", "")
	lineas_limpias: list[str] = []

	for linea in contenido.splitlines():
		linea = linea.strip()
		if not linea or linea.startswith(">"):
			continue
		lineas_limpias.append(linea)

	return "".join(lineas_limpias).upper()


def posiciones_motivo(secuencia: str, motivo: str = MOTIVO_TATA) -> list[int]:
	"""Devuelve los índices de inicio (0-based) de todas las apariciones del motivo."""
	posiciones: list[int] = []
	inicio_busqueda = 0

	while True:
		indice = secuencia.find(motivo, inicio_busqueda)
		if indice == -1:
			break
		posiciones.append(indice)
		inicio_busqueda = indice + 1

	return posiciones


def identificar_regiones_promotoras(
	secuencia: str, motivo: str = MOTIVO_TATA
) -> list[dict[str, int | str]]:
	"""
	Arma regiones con pares consecutivos de cajas TATA.
	Cada región empieza en una caja TATA y termina al finalizar la siguiente.
	"""
	posiciones = posiciones_motivo(secuencia, motivo)
	regiones: list[dict[str, int | str]] = []

	for i in range(len(posiciones) - 1):
		inicio = posiciones[i]
		fin_inclusivo = posiciones[i + 1] + len(motivo) - 1
		texto = secuencia[inicio : fin_inclusivo + 1]
		regiones.append(
			{
				"inicio": inicio,
				"fin": fin_inclusivo,
				"secuencia": texto,
			}
		)

	return regiones


def ejecutar_cli(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(
		description="Identifica regiones promotoras delimitadas por cajas TATA consecutivas."
	)
	parser.add_argument("archivo", help="Ruta a archivo con secuencia de ADN (texto o FASTA).")
	args = parser.parse_args(argv)

	secuencia = leer_secuencia_desde_archivo(args.archivo)
	regiones = identificar_regiones_promotoras(secuencia)

	if not regiones:
		print("No se encontraron regiones promotoras completas (menos de 2 cajas TATA).")
		return 1

	print(f"Se encontraron {len(regiones)} region(es) promotora(s):")
	for i, region in enumerate(regiones, start=1):
		print(f"{i}. {region['secuencia']} (inicio={region['inicio']}, fin={region['fin']})")

	return 0


if __name__ == "__main__":
	raise SystemExit(ejecutar_cli())
