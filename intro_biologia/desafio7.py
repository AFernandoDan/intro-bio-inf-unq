from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class RegistroMotivo:
    identificador: str
    secuencia: str
    coincidencias: list[tuple[int, str]]


def crear_regex_desde_motivo(motivo_biologico: str) -> re.Pattern[str]:
    if not motivo_biologico or not motivo_biologico.strip():
        raise ValueError("El motivo biologico no puede estar vacio.")

    motivo = motivo_biologico.strip().upper()
    patron_regex = motivo.replace("{", "[^").replace("}", "]")
    patron_solapado = f"(?=({patron_regex}))"
    return re.compile(patron_solapado)


def buscar_motivo_en_secuencia(regex: re.Pattern[str], secuencia: str) -> list[tuple[int, str]]:
    resultados: list[tuple[int, str]] = []
    for coincidencia in regex.finditer(secuencia):
        resultados.append((coincidencia.start() + 1, coincidencia.group(1)))
    return resultados


def parsear_fasta(texto: str) -> list[tuple[str, str]]:
    registros: list[tuple[str, str]] = []
    encabezado: Optional[str] = None
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


def leer_archivo_texto(ruta: Path) -> str:
    if not ruta.exists():
        cwd = Path.cwd()
        raise ValueError(
            f"No existe el archivo de entrada: {ruta}. Directorio actual: {cwd}"
        )
    if not ruta.is_file():
        raise ValueError(f"La ruta de entrada no es un archivo: {ruta}")

    try:
        return ruta.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"No se pudo leer {ruta} como UTF-8. Usa un archivo de texto plano en UTF-8."
        ) from exc


def descargar_fasta_uniprot(uniprot_id: str) -> str:
    uniprot_id_limpio = uniprot_id.strip().upper()
    if not uniprot_id_limpio:
        raise ValueError("El identificador de UniProt no puede estar vacio.")

    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id_limpio}.fasta"
    try:
        with urllib.request.urlopen(url, timeout=10) as respuesta:
            if getattr(respuesta, "status", 200) != 200:
                raise ValueError(f"No se pudo descargar UniProt {uniprot_id_limpio}: HTTP {respuesta.status}")
            contenido = respuesta.read().decode("utf-8")
            if not contenido.strip():
                raise ValueError(f"El FASTA de UniProt {uniprot_id_limpio} esta vacio.")
            return contenido
    except urllib.error.HTTPError as exc:
        raise ValueError(f"UniProt no encontro el ID {uniprot_id_limpio}.") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"No se pudo conectar a UniProt: {exc}") from exc


def leer_entrada(args: argparse.Namespace) -> list[tuple[str, str]]:
    fuentes = [bool(args.ids), bool(args.input), bool(args.secuencia), bool(args.stdin)]
    if sum(fuentes) != 1:
        raise ValueError("Debes indicar exactamente una fuente: --ids, --input, --secuencia o --stdin.")

    if args.ids:
        return [(identificador.strip(), "") for identificador in args.ids if identificador.strip()]

    if args.input:
        texto = leer_archivo_texto(Path(args.input))
        registros = parsear_fasta(texto)
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
        registros = parsear_fasta(texto)
        if registros:
            return registros
        secuencia = "".join(texto.split()).upper()
        if not secuencia:
            raise ValueError("No se recibio secuencia por stdin.")
        return [(args.id, secuencia)]

    raise ValueError("Debes indicar una fuente de secuencia.")


def procesar_registro(identificador: str, secuencia: str, regex: re.Pattern[str]) -> RegistroMotivo:
    if not secuencia:
        fasta_texto = descargar_fasta_uniprot(identificador)
        registros = parsear_fasta(fasta_texto)
        if not registros:
            raise ValueError(f"No se encontro secuencia para UniProt {identificador}.")
        identificador, secuencia = registros[0]

    coincidencias = buscar_motivo_en_secuencia(regex, secuencia)
    return RegistroMotivo(identificador=identificador, secuencia=secuencia, coincidencias=coincidencias)


def procesar_registros(entradas: list[tuple[str, str]], regex: re.Pattern[str]) -> list[RegistroMotivo]:
    if not entradas:
        return []

    resultados: list[RegistroMotivo] = []
    with ThreadPoolExecutor(max_workers=min(8, len(entradas))) as executor:
        future_results = executor.map(
            lambda registro: procesar_registro(registro[0], registro[1], regex),
            entradas,
        )
        resultados = list(future_results)
    return resultados


def resumir_secuencia(secuencia: str, longitud_visible: int = 24) -> str:
    if len(secuencia) <= longitud_visible:
        return secuencia

    mitad = max(1, (longitud_visible - 3) // 2)
    inicio = secuencia[:mitad]
    fin = secuencia[-mitad:]
    return f"{inicio}...{fin}"


def formatear_texto(registros: list[RegistroMotivo]) -> str:
    bloques: list[str] = []
    for registro in registros:
        lineas = [f"ID: {registro.identificador}", f"Secuencia: {resumir_secuencia(registro.secuencia)}"]
        if registro.coincidencias:
            lineas.append("Coincidencias:")
            for posicion, texto in registro.coincidencias:
                lineas.append(f"  - Posicion {posicion}: {texto}")
        else:
            lineas.append("Coincidencias: ninguna")
        bloques.append("\n".join(lineas))
    return "\n\n".join(bloques) + "\n"


def formatear_json(registros: list[RegistroMotivo], motivo_biologico: str) -> str:
    payload = [
        {
            "id": registro.identificador,
            "secuencia": registro.secuencia,
            "motivo": motivo_biologico,
            "coincidencias": [
                {"posicion": posicion, "texto": texto}
                for posicion, texto in registro.coincidencias
            ],
        }
        for registro in registros
    ]
    return json.dumps(payload, ensure_ascii=True, indent=2) + "\n"


def serializar_salida(registros: list[RegistroMotivo], formato: str, motivo_biologico: str) -> str:
    serializadores = {
        "texto": lambda datos: formatear_texto(datos),
        "json": lambda datos: formatear_json(datos, motivo_biologico),
    }
    if formato not in serializadores:
        raise ValueError(f"Formato no soportado: {formato}")
    return serializadores[formato](registros)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="buscador-motivo-uniprot",
        description="Busca motivos biologicos en proteinas UniProt o en FASTA local.",
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        help="Lista de identificadores UniProt para descargar y analizar.",
    )
    parser.add_argument(
        "--input",
        help="Archivo FASTA de entrada con una o varias proteinas.",
    )
    parser.add_argument(
        "--secuencia",
        help="Secuencia de aminoacidos directa (una sola letra).",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Leer secuencia o FASTA desde la entrada estandar.",
    )
    parser.add_argument(
        "--id",
        default="secuencia",
        help="Identificador para la secuencia directa o stdin cuando no hay FASTA.",
    )
    parser.add_argument(
        "--motivo",
        required=True,
        help="Motivo biologico al estilo Rosalind, por ejemplo N{P}[ST]{P}.",
    )
    parser.add_argument(
        "--formato",
        choices=["texto", "json"],
        default="texto",
        help="Formato de salida.",
    )
    parser.add_argument("-o", "--output", help="Archivo de salida; por defecto imprime en stdout.")
    return parser


def ejecutar_cli(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)

    try:
        entradas = leer_entrada(args)
        regex = crear_regex_desde_motivo(args.motivo)
        resultados = procesar_registros(entradas, regex)
        salida = serializar_salida(resultados, args.formato, args.motivo)
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
