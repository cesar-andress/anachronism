# src/h2_semantics.py
"""
Heurísticas para la hipótesis H2:
- Distinguir usos histórico-doctrinales de usos metafóricos/anacrónicos
  de términos como 'nazi', 'fascista', 'comunista', etc.

Devuelve una etiqueta:
- H2_HISTORICO: referencia a hechos/doctrinas históricas.
- H2_METAFORICO_ANACRONICO: uso como insulto/hipérbole en contextos actuales.
- H2_NO_CLASIFICADO: sin suficiente evidencia.
"""

from __future__ import annotations
from typing import Literal, Dict, Any
import re

H2Label = Literal["H2_HISTORICO", "H2_METAFORICO_ANACRONICO", "H2_NO_CLASIFICADO"]

# ---------------------------------------------------------------------------
# Términos ideológicos núcleo (sustantivos y adjetivos)
# ---------------------------------------------------------------------------
TARGET_IDEO_TERMS = [
    # Núcleo clásico
    r"\bnazi(s|mo)?\b",
    r"\bfascist(a|as|o|os|mo)?\b",
    r"\bcomunist(a|as|o|os|mo)?\b",
    r"\bfranquist(a|as|o|os|mo)?\b",

    # Vocabulario coloquial/político español
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
# Indicadores de contexto histórico/doctrinal "serio"
# ---------------------------------------------------------------------------
HISTORICAL_CONTEXT_TERMS = [
    # Líderes y figuras históricas
    r"\bhitler\b",
    r"\badolf hitler\b",
    r"\bmussolini\b",
    r"\bbenito mussolini\b",
    r"\bfranco\b",
    r"\bgeneral[ií]simo\b",
    r"\bstalin\b",
    r"\bj[oó]s?ef stalin\b",
    r"\blenin\b",
    r"\bmao\b",
    r"\bmao tse[- ]tung\b",
    r"\bpol pot\b",
    r"\bgoebbels\b",
    r"\bhimmler\b",

    # Partidos y organizaciones
    r"\bpartido nazi\b",
    r"\bpartido nacionalsocialista\b",
    r"\bnsdap\b",
    r"\bfalange\b",
    r"\bfalange espa[nñ]ola\b",
    r"\bpc[eef]\b",      # PCE, PCF, etc.
    r"\bpartido comunista\b",

    # Regímenes, ideologías, doctrinas
    r"\breg[ií]men\b",
    r"\bregimen\b",  # por si se escapa sin tilde
    r"\bdictadura(s)?\b",
    r"\bdictatorial(es)?\b",
    r"\btotalitarismo(s)?\b",
    r"\btotalitario(s)?\b",
    r"\bideolog[ií]a(s)?\b",
    r"\bdoctrina(s)?\b",
    r"\bteor[ií]a(s)? pol[ií]tica(s)?\b",
    r"\bnacionalsocialismo\b",
    r"\bnazismo\b",
    r"\bfascismo\b",
    r"\bcomunismo\b",
    r"\bestalinismo\b",
    r"\bmao[ií]smo\b",

    # Estados e instituciones históricas
    r"\bii? guerra mundial\b",
    r"\bsegunda guerra\b",
    r"\bsegunda guerra mundial\b",
    r"\b1[9]{2}9\b",            # referencias a 1929, etc. (muy genérico, pero poco frecuente)
    r"\bholocausto\b",
    r"\bshoah\b",
    r"\bgueto(s)?\b",
    r"\bcampos? de concentraci[oó]n\b",
    r"\bsoluci[oó]n final\b",
    r"\btercer reich\b",
    r"\biii reich\b",

    r"\bsovi[eé]tic[oa]s?\b",
    r"\buni[oó]n sovi[eé]tica\b",
    r"\burr?s?\b",           # URSS escrito raro
    r"\burgss?\b",           # por si acaso
    r"\bold? bloc sovi[eé]tico\b",
    r"\bgulag(s)?\b",

    # Referencias históricas hispanas
    r"\bguerra civil\b",
    r"\bguerra civil espa[nñ]ola\b",
    r"\bfranquismo\b",
    r"\btransici[oó]n espa[nñ]ola\b",
]

# ---------------------------------------------------------------------------
# Indicadores de uso metafórico/anacrónico (contextos triviales / cotidianos)
# ---------------------------------------------------------------------------
METAPHORICAL_CONTEXT_PATTERNS = [
    # Vida cotidiana, trabajo, estudios
    r"\bprofe(sor|sora)?\b",
    r"\bprofes\b",
    r"\bmaestr[oa]s?\b",
    r"\bexamen(es)?\b",
    r"\bselectividad\b",
    r"\bclase(s)?\b",
    r"\bcolegio\b",
    r"\binstituto\b",
    r"\buniversidad\b",
    r"\buni\b",

    r"\bjef[ea]s?\b",
    r"\bcompa[nñ]er[oa]s?\b",
    r"\btrabaj[oa]\b",
    r"\bempresa\b",
    r"\boficina\b",
    r"\brrhh\b",

    # Familia, pareja, entorno personal
    r"\bmadre\b",
    r"\bpadre\b",
    r"\bherman[oa]s?\b",
    r"\bpareja\b",
    r"\bnovi[oa]s?\b",
    r"\bfamilia(s)?\b",
    r"\bsuegr[oa]s?\b",

    # Barrio, convivencia, ocio
    r"\bvecin[oa]s?\b",
    r"\bcomunidad de vecinos\b",
    r"\bpiscina comunitaria\b",
    r"\bportero\b",
    r"\bconserje\b",

    r"\bf[úu]tbol\b",
    r"\bárbitro(s)?\b",
    r"\bentrenador(es)?\b",
    r"\bequip[oa]s?\b",
    r"\bafici[oó]n\b",

    # Burocracia, normas, cosas del día a día
    r"\bmult[ao]s?\b",
    r"\bimpuest[oa]s?\b",
    r"\btr[aá]mites?\b",
    r"\bburocracia\b",
    r"\bformularios?\b",
    r"\bventanilla\b",

    # COVID, restricciones, policía de lo cotidiano
    r"\bmascarillas?\b",
    r"\brestricciones?\b",
    r"\btoque de queda\b",
    r"\bpolic[ií]a\b",
    r"\bguardia\b",

    # Internet / redes como contexto trivial
    r"\bmoderador(es)?\b",
    r"\badmins?\b",
    r"\bforo(s)?\b",
    r"\bgrupo de whatsapp\b",
    r"\bwhatsapp\b",
    r"\btelegram\b",
    r"\bdiscord\b",
    r"\bred(es)? sociales\b",

    # Otros contextos claramente no históricos
    r"\brestaurante(s)?\b",
    r"\bbar(es)?\b",
    r"\bdiscoteca(s)?\b",
    r"\bmetro\b",
    r"\bbus\b",
]

# ---------------------------------------------------------------------------
# Estructuras típicas de etiqueta metafórica / hiperbólica
# ---------------------------------------------------------------------------
METAPHORICAL_FRAMES = [
    r"\best[oa]s?\s+nazis\b",
    r"\best[oa]s?\s+fascistas\b",
    r"\best[oa]s?\s+comunistas\b",
    r"\best[oa]s?\s+fachas\b",
    r"\bsois unos?\s+\w+\b",
    r"\bmenud[oa]s?\s+\w+\b",
    r"\bmanda narices\b",
    r"\bmanda huevos\b",
    r"\bde manual\b",
    r"\bde libro\b",
    r"\bde traca\b",
    r"\bvaya\s+\w+\b",
    r"\bvaya tela\b",
    r"\bno se puede ser m[aá]s\b",
    r"\bcomo si fuera[n]?\s+nazis\b",
    r"\bcomo si fuera[n]?\s+fascistas\b",
]


def _match_any(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def contains_target_term(text: str) -> bool:
    return _match_any(TARGET_IDEO_TERMS, text)


def has_historical_context(text: str) -> bool:
    """Indicios de que se habla del fenómeno histórico/doctrinal."""
    return _match_any(HISTORICAL_CONTEXT_TERMS, text)


def has_metaphorical_context(text: str) -> bool:
    """
    Indicios de uso metafórico/anacrónico:
    - términos ideológicos aparecen junto a contextos triviales o cotidianos
    - frames discursivos típicos de hipérbole.
    """
    if _match_any(METAPHORICAL_CONTEXT_PATTERNS, text):
        return True
    if _match_any(METAPHORICAL_FRAMES, text):
        return True
    return False


def classify_h2(text: str) -> Dict[str, Any]:
    """
    Clasifica un tuit respecto a H2:

    - h2_label: H2_HISTORICO / H2_METAFORICO_ANACRONICO / H2_NO_CLASIFICADO
    - h2_has_target: aparece algún término ideológico núcleo
    - h2_historical_context: indicios de contexto histórico/doctrinal
    - h2_metaphorical_context: indicios de contexto metafórico/anacrónico
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    t = text.lower().strip()

    has_target = contains_target_term(t)
    hist = has_historical_context(t)
    meta = has_metaphorical_context(t)

    if not has_target:
        label: H2Label = "H2_NO_CLASIFICADO"
    else:
        # Si hay contexto histórico explícito, priorizamos esa lectura
        if hist:
            label = "H2_HISTORICO"
        # Si no hay contexto histórico pero sí metafórico, lo leemos como anacrónico
        elif meta:
            label = "H2_METAFORICO_ANACRONICO"
        else:
            # Aparece el término, pero no detectamos contexto claro
            label = "H2_NO_CLASIFICADO"

    return {
        "h2_label": label,
        "h2_has_target": has_target,
        "h2_historical_context": hist,
        "h2_metaphorical_context": meta,
    }
