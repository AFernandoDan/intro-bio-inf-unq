from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .desafio5 import ChouFasmanPredictor


@dataclass(frozen=True)
class RegistroPrediccion:
    identificador: str
    secuencia: str
    estructura: str


def _parsear_fasta(texto: str) -> list[tuple[str, str]]:
    registros: list[tuple[str, str]] = []
    encabezado: str | None = None
    secuencia_actual: list[str] = []

    for linea in texto.splitlines():
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue

        if linea_limpia.startswith(">"):
            if encabezado is not None:
                registros.append((encabezado, "".join(secuencia_actual).upper()))
            encabezado = linea_limpia[1:].strip() or "secuencia"
            secuencia_actual = []
            continue

        secuencia_actual.append(linea_limpia)

    if encabezado is not None:
        registros.append((encabezado, "".join(secuencia_actual).upper()))

    return registros


def _leer_entrada(args: argparse.Namespace) -> list[tuple[str, str]]:
    if args.input:
        texto = _leer_archivo_texto(Path(args.input))
        registros = _parsear_fasta(texto)
        if registros:
            return registros
        secuencia = "".join(texto.split()).upper()
        if not secuencia:
            raise ValueError("El archivo de entrada esta vacio.")
        return [(args.id, secuencia)]

    if args.secuencia:
        return [(args.id, args.secuencia.strip().upper())]

    if args.stdin:
        texto = sys.stdin.read()
        registros = _parsear_fasta(texto)
        if registros:
            return registros
        secuencia = "".join(texto.split()).upper()
        if not secuencia:
            raise ValueError("No se recibio secuencia por stdin.")
        return [(args.id, secuencia)]

    raise ValueError("Debes indicar --input, --secuencia o --stdin.")


def _leer_archivo_texto(ruta: Path) -> str:
    if not ruta.exists():
        cwd = Path.cwd()
        raise ValueError(
            f"No existe el archivo de entrada: {ruta}. "
            f"Directorio actual: {cwd}"
        )
    if not ruta.is_file():
        raise ValueError(f"La ruta de entrada no es un archivo: {ruta}")

    try:
        return ruta.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"No se pudo leer {ruta} como UTF-8. "
            "Usa un archivo de texto plano en UTF-8."
        ) from exc


def _predecir_registros(entradas: Iterable[tuple[str, str]]) -> list[RegistroPrediccion]:
    predictor = ChouFasmanPredictor()
    resultados: list[RegistroPrediccion] = []

    for identificador, secuencia in entradas:
        estructura = predictor.predecir(secuencia).secondary_structure_string
        resultados.append(
            RegistroPrediccion(
                identificador=identificador,
                secuencia=secuencia,
                estructura=estructura,
            )
        )

    return resultados


def _formatear_texto(registros: list[RegistroPrediccion]) -> str:
    bloques: list[str] = []
    for registro in registros:
        bloques.append(
            "\n".join(
                [
                    f"ID: {registro.identificador}",
                    f"Secuencia:  {registro.secuencia}",
                    f"Estructura: {registro.estructura}",
                ]
            )
        )
    return "\n\n".join(bloques) + "\n"


def _formatear_fasta(registros: list[RegistroPrediccion]) -> str:
    lineas: list[str] = []
    for registro in registros:
        lineas.append(f">{registro.identificador}")
        lineas.append(registro.secuencia)
        lineas.append(f">{registro.identificador}_pred_ss3")
        lineas.append(registro.estructura)
    return "\n".join(lineas) + "\n"


def _formatear_tsv(registros: list[RegistroPrediccion]) -> str:
    lineas = ["id\tposicion\tresiduo\testructura"]
    for registro in registros:
        for indice, (residuo, estructura) in enumerate(
            zip(registro.secuencia, registro.estructura),
            start=1,
        ):
            lineas.append(f"{registro.identificador}\t{indice}\t{residuo}\t{estructura}")
    return "\n".join(lineas) + "\n"


def _formatear_json(registros: list[RegistroPrediccion]) -> str:
    payload = [
        {
            "id": registro.identificador,
            "secuencia": registro.secuencia,
            "estructura_secundaria": registro.estructura,
        }
        for registro in registros
    ]
    return json.dumps(payload, ensure_ascii=True, indent=2) + "\n"


def _serializar_salida(registros: list[RegistroPrediccion], formato: str) -> str:
    serializadores = {
        "texto": _formatear_texto,
        "fasta": _formatear_fasta,
        "tsv": _formatear_tsv,
        "json": _formatear_json,
    }
    if formato not in serializadores:
        raise ValueError(f"Formato no soportado: {formato}")
    return serializadores[formato](registros)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prediccion-ss3",
        description="Predice estructura secundaria (H/B/L) con Chou-Fasman.",
    )
    parser.add_argument("-i", "--input", help="Archivo de entrada (FASTA o secuencia cruda).")
    parser.add_argument("-s", "--secuencia", help="Secuencia directa de aminoacidos (una letra).")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Leer desde entrada estandar (FASTA o secuencia cruda).",
    )
    parser.add_argument("--id", default="secuencia", help="Identificador para secuencia directa.")
    parser.add_argument(
        "-f",
        "--formato",
        choices=["texto", "fasta", "tsv", "json"],
        default="texto",
        help="Formato de salida.",
    )
    parser.add_argument("-o", "--output", help="Archivo de salida; por defecto imprime en stdout.")
    return parser


def ejecutar_cli(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)

    fuentes = [bool(args.input), bool(args.secuencia), bool(args.stdin)]
    if sum(fuentes) != 1:
        parser.error("Debes indicar exactamente una fuente: --input, --secuencia o --stdin.")

    try:
        entradas = _leer_entrada(args)
        resultados = _predecir_registros(entradas)
        salida = _serializar_salida(resultados, args.formato)
        if args.output:
            Path(args.output).write_text(salida, encoding="utf-8")
        else:
            print(salida, end="")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Error de sistema de archivos: {exc}", file=sys.stderr)
        return 2

    return 0


def main() -> int:
    return ejecutar_cli()


if __name__ == "__main__":
    raise SystemExit(main())
