# src/label_functions.py
"""
Funciones heurísticas para clasificar los tuits según su función:

- EVALUATIVO: uso insultante / descalificador / expresivo.
- DEFINICIONAL: uso analítico / explicativo / doctrinal.
- MIXTO: contiene rasgos de ambas.
- OTRO: no encaja claramente (neutro, informativo, etc.).

Estas reglas son simples y transparentes, útiles para un TFM/tesis:
luego puedes afinarlas o combinarlas con anotación manual.
"""

from __future__ import annotations
from typing import Literal, Dict, Any
import re


LabelFuncion = Literal["EVALUATIVO", "DEFINICIONAL", "MIXTO", "OTRO"]


# Listas de patrones muy simples (puedes ampliarlas)
INSULT_PATTERNS = [
    r"\bde mierda\b",
    r"\bput[oa]s?\b",
    r"\beras un[ao]?\b",
    r"\bsois unos\b",
    r"\bsois unas\b",
    r"\bmaldit[oa]s?\b",
    r"\bimb[eé]cil(es)?\b",
    r"\bidiot[ao]s?\b",
    r"\bgilipollas\b",
    r"\bpayas[ao]s?\b",
    r"\bescoria\b",
    r"\bbasura\b",
]

# Patrones típicos de usos definicionales / analíticos
DEFINITION_PATTERNS = [
    r"\bes un sistema\b",
    r"\bes una doctrina\b",
    r"\bes una ideolog[ií]a\b",
    r"\bse caracteriza por\b",
    r"\bse define como\b",
    r"\bse puede definir como\b",
    r"\bconsiste en\b",
    r"\bdoctrina que\b",
    r"\bideolog[ií]a que\b",
    r"\bse entiende por\b",
]

# Términos ideológicos típicamente usados como etiqueta descalificadora
IDEOLOGICAL_INSULT_TERMS = [
    # “ismos” clásicos
    r"\bfascism(o|os)?\b",
    r"\bfascist(a|as|o|os)?\b",
    r"\bnazism(o|os)?\b",
    r"\bnazi(s)?\b",
    r"\bcomunism(o|os)?\b",
    r"\bcomunist(a|as|o|os)?\b",
    r"\bfranquism(o|os)?\b",
    r"\bfranquist(a|as|o|os)?\b",

    # Insultos ideológicos coloquiales muy españoles
    r"\bfacha(s|zo|zos|zuela|zuelos)?\b",
    r"\broj[oa]s?\b",
    r"\brojill[oa]s?\b",
    r"\bprogre(s|zuelos?)?\b",

    # Latino-españoles habituales en discurso político
    r"\bbolivarian[oa]s?\b",
    r"\bchavist(a|as|o|os)?\b",
    r"\bsocialcomunist(a|as|o|os)?\b",

    # Campos semánticos: ultra / extrema
    r"\bultra(s)?\b",
    r"\bultraderech[ae]\b",
    r"\bultraizquierd[ae]\b",

    # Ideologemas recurrentes
    r"\bneoliberal(es)?\b",
    r"\bpopulist(a|as|o|os)?\b",
]



# Patrones de estructuras descalificadoras frecuentes
IDEOLOGICAL_INSULT_PATTERNS = [
    r"eres un[oa]?\s+\w+",
    r"sois unos?\s+\w+",
    r"estos\s+\w+",
    r"menud[oa]s?\s+\w+",
    r"vaya\s+\w+",
    r"los\s+\w+\s+de turno",
    r"\b\w+\s+de manual\b",
]


def _match_any(patterns: list[str], text: str) -> bool:
    """Devuelve True si alguno de los patrones aparece en el texto."""
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def detect_definitional(text: str) -> bool:
    """
    Indicio de uso definicional/analítico.
    Busca estructuras típicas de definición de conceptos.
    """
    if not text:
        return False

    t = text.lower()
    return _match_any(DEFINITION_PATTERNS, t)


def detect_ideological_insult(text: str) -> bool:
    """
    Detecta insultos basados en términos ideológicos.
    Tiene en cuenta tanto la presencia de ciertos términos
    como estructuras de descalificación.
    """
    if not text:
        return False

    t = text.lower()

    # 1. Si aparece un término ideológico como sustantivo (modo insulto)
    if any(re.search(p, t) for p in IDEOLOGICAL_INSULT_TERMS):
        # Sólo cuenta como insulto si no hay indicios claros de definición
        if not detect_definitional(t):
            return True

    # 2. Patrones de descalificación (eres X / vaya X / etc.)
    if any(re.search(p, t) for p in IDEOLOGICAL_INSULT_PATTERNS):
        return True

    return False


def detect_insult(text: str) -> bool:
    """
    Indicio de uso evaluativo/insultante.
    Combina insulto vulgar + insulto ideológico.
    """
    if not text:
        return False

    t = text.lower()

    # Patrones “genéricos” de insulto
    if _match_any(INSULT_PATTERNS, t):
        return True

    # Insulto ideológico (facha, nazi, comunista, etc.)
    if detect_ideological_insult(t):
        return True

    return False


def classify_function(text: str) -> Dict[str, Any]:
    """
    Clasifica un tuit según función pragmática:

    - label_funcion: EVALUATIVO / DEFINICIONAL / MIXTO / OTRO
    - has_insult: True/False
    - has_def_pattern: True/False
    - length_chars: longitud en caracteres
    - length_tokens: nº aproximado de palabras (split por espacios)
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    stripped = text.strip()
    length_chars = len(stripped)
    length_tokens = len(stripped.split()) if stripped else 0

    has_insult = detect_insult(stripped)
    has_def = detect_definitional(stripped)

    if has_insult and not has_def:
        label: LabelFuncion = "EVALUATIVO"
    elif has_def and not has_insult:
        label = "DEFINICIONAL"
    elif has_insult and has_def:
        label = "MIXTO"
    else:
        label = "OTRO"

    return {
        "label_funcion": label,
        "has_insult": has_insult,
        "has_def_pattern": has_def,
        "length_chars": length_chars,
        "length_tokens": length_tokens,
    }
