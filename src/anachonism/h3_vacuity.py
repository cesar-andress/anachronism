# src/h3_vacuity.py
"""
Heurísticas para la hipótesis H3:
- Detectar "vacuidad semántica" en el uso de términos ideológicos.
- Distinguir usos ligeros / poco densos de usos más desarrollados.

Devuelve una etiqueta:

- H3_VACIO: uso ligero, poco contextualizado, casi solo etiqueta ideológica.
- H3_DENSO: uso relativamente desarrollado, con conectores, referencias a hechos, etc.
- H3_NO_CLASIFICADO: sin evidencia suficiente para decidir.

Estas heurísticas son simples y explicables para un TFM; no pretenden ser
un modelo lingüístico exhaustivo, sino un indicador aproximado.
"""

from __future__ import annotations
from typing import Literal, Dict, Any
import re

H3Label = Literal["H3_VACIO", "H3_DENSO", "H3_NO_CLASIFICADO"]

# ---------------------------------------------------------------------------
# Términos ideológicos núcleo (sustantivos y adjetivos)
# ---------------------------------------------------------------------------
# Reutilizamos la idea de términos ideológicos núcleo
# Reutilizamos la idea de términos ideológicos núcleo (ampliados para política española)
TARGET_IDEO_TERMS = [
    r"\bfascist(a|as|o|os|mo)?\b",
    r"\bnazi(s|mo)?\b",
    r"\bcomunist(a|as|o|os|mo)?\b",
    r"\bfranquist(a|as|o|os|mo)?\b",

    r"\bfacha(s)?\b",
    r"\broj[oa]s?\b",
    r"\brojill[oa]s?\b",
    r"\bprogre(s)?\b",

    r"\bbolivarian[oa]s?\b",
    r"\bchavist(a|as|o|os)?\b",
    r"\bsocialcomunist(a|as|o|os)?\b",
    r"\bneoliberal(es)?\b",
    r"\bultraderech[ae]\b",
    r"\bultraizquierd[ae]\b",
    r"\bpopulist(a|as|o|os)?\b",
]



# ---------------------------------------------------------------------------
# Conectores explicativos / argumentativos sencillos
# ---------------------------------------------------------------------------
CONNECTIVES = [
    # Causales / explicativos
    r"\bporque\b",
    r"\bya que\b",
    r"\bdebido a\b",
    r"\bgracias a\b",
    r"\bpor eso\b",
    r"\bpor ello\b",
    r"\bpor esta raz[oó]n\b",

    # Consecutivos / inferenciales
    r"\bpor tanto\b",
    r"\bpor lo tanto\b",
    r"\bpor consiguiente\b",
    r"\bde modo que\b",
    r"\bde manera que\b",
    r"\bas[ií] que\b",
    r"\bentonces\b",

    # Reformulativos
    r"\bes decir\b",
    r"\bo sea\b",
    r"\ben otras palabras\b",
    r"\bo, mejor dicho\b",

    # Contraargumentativos
    r"\bpero\b",
    r"\bsin embargo\b",
    r"\bno obstante\b",
    r"\baunque\b",
    r"\ben cambio\b",
    r"\bpor el contrario\b",

    # Aditivos (suelen acompañar enumeraciones y argumentos)
    r"\badem[aá]s\b",
    r"\bencima\b",
    r"\bsobre todo\b",
    r"\bincluso\b",
]

# ---------------------------------------------------------------------------
# Indicadores de referencia a hechos / contexto (muy simples)
# ---------------------------------------------------------------------------
EVENT_CLUES = [
    # Procesos políticos e institucionales genéricos
    r"\belecciones?\b",
    r"\belecciones generales\b",
    r"\belecciones auton[oó]micas\b",
    r"\belecciones municipales\b",
    r"\brefer[eé]ndum\b",
    r"\breferendum\b",
    r"\bgobierno\b",
    r"\bgobiernos\b",
    r"\boposici[oó]n\b",
    r"\bparlamento\b",
    r"\bcongreso\b",
    r"\bsenado\b",
    r"\bhemiciclo\b",
    r"\bley(es)?\b",
    r"\bdecreto-?ley\b",
    r"\bconstituci[oó]n\b",
    r"\btribunal constitucional\b",

    # Actores, partidos y líderes (España + genéricos)
    r"\bpsoe\b",
    r"\bpp\b",
    r"\bvox\b",
    r"\bciudadanos\b",
    r"\bcs\b",
    r"\bpodemos\b",
    r"\bunidas podemos\b",
    r"\bsumar\b",
    r"\bjunts\b",
    r"\berc\b",
    r"\bbildu\b",

    r"\bpedro s[aá]nchez\b",
    r"\bs[aá]nchez\b",
    r"\bfeij[oó]o\b",
    r"\babascal\b",
    r"\bayuso\b",
    r"\bd[ií]az\b",
    r"\bmontero\b",
    r"\biglesias\b",

    # Geopolítica, conflictos, organismos
    r"\bue\b",
    r"\bun[ií]on europea\b",
    r"\bnato\b",
    r"\botan\b",
    r"\bucrania\b",
    r"\brusia\b",
    r"\bputin\b",
    r"\btrump\b",
    r"\bbiden\b",
    r"\bguerra\b",
    r"\bconflicto\b",
    r"\bfrente\b",

    # Economía, crisis, políticas públicas
    r"\bcrisis\b",
    r"\binflaci[oó]n\b",
    r"\bparo\b",
    r"\bdesempleo\b",
    r"\bsubida de impuestos\b",
    r"\bimpuestos\b",
    r"\bsalario\b",
    r"\bsm[ií]n\b",
    r"\bpensiones\b",
    r"\bsubvencione?s?\b",

    # COVID y otras coyunturas
    r"\bpandemia\b",
    r"\bcovid\b",
    r"\bcoronavirus\b",
    r"\bestado de alarma\b",
    r"\bconfinamiento\b",
    r"\brestricciones?\b",
    r"\btoque de queda\b",

    # Territorio, instituciones concretas
    r"\bmoncloa\b",
    r"\bferraz\b",
    r"\bg[eé]nova\b",
    r"\bcongreso de los diputados\b",
    r"\bparlamento europeo\b",
    r"\bcomunidad de madrid\b",
    r"\bcatalu[ñn]a\b",
    r"\bindependentismo\b",
]

DIGITS_PATTERN = r"\d"  # cualquier número (fechas, porcentajes, etc.)


def _match_any(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def contains_target_term(text: str) -> bool:
    return _match_any(TARGET_IDEO_TERMS, text)


def has_connectives(text: str) -> bool:
    return _match_any(CONNECTIVES, text)


def has_event_clues(text: str) -> bool:
    """
    Indicios muy básicos de contexto político o factual:
    - palabras clave de procesos, actores, lugares o conflictos
    - aparición de dígitos (años, porcentajes, cifras)
    """
    if _match_any(EVENT_CLUES, text):
        return True
    if re.search(DIGITS_PATTERN, text):
        return True
    return False


def has_hashtags_or_mentions(text: str) -> bool:
    return "#" in text or "@" in text


def classify_h3(text: str) -> Dict[str, Any]:
    """
    Clasifica un tuit respecto a H3 (vacuidad semántica):

    - h3_label: H3_VACIO / H3_DENSO / H3_NO_CLASIFICADO
    - h3_length_tokens: nº aproximado de palabras
    - h3_has_connectives: True/False
    - h3_has_event_clues: True/False
    - h3_has_hashtags_or_mentions: True/False
    - h3_has_ideo_term: True/False
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    t = text.strip()
    t_lower = t.lower()
    tokens = t.split()
    length_tokens = len(tokens)

    has_ideo = contains_target_term(t_lower)
    conn = has_connectives(t_lower)
    event = has_event_clues(t_lower)
    tags = has_hashtags_or_mentions(t)

    # Si ni siquiera aparece el término ideológico, no evaluamos vacuidad
    if not has_ideo:
        label: H3Label = "H3_NO_CLASIFICADO"
    else:
        # Heurística para "vacuidad":
        # - tuit muy corto, o
        # - relativamente corto y sin conectores ni referencias a hechos
        if length_tokens <= 8:
            label = "H3_VACIO"
        elif length_tokens <= 15 and not conn and not event:
            label = "H3_VACIO"
        # Heurística para "densidad":
        # - tuit largo y con conectores o referencias a hechos
        elif length_tokens >= 20 and (conn or event):
            label = "H3_DENSO"
        else:
            label = "H3_NO_CLASIFICADO"

    return {
        "h3_label": label,
        "h3_length_tokens": length_tokens,
        "h3_has_connectives": conn,
        "h3_has_event_clues": event,
        "h3_has_hashtags_or_mentions": tags,
        "h3_has_ideo_term": has_ideo,
    }
