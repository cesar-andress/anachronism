# src/fallacies.py

"""
Heurísticas muy simples para detectar posibles falacias argumentativas
en tuits políticos, pensadas para un TFM:

- Ad antiquitatem (tradición)
- Ad baculum (miedo / fuerza)
- Ad consequentiam (consecuencias)
- Ad crumenam (riqueza)
- Ad hominem / ad personam (contra la persona)
- Ad ignorantiam (ignorancia)
- Ad lazarum (pobreza)
- Ad logicam (rechazo por mala lógica)
- Ad misericordiam (piedad)
- Ad nauseam (repetición)
- Ad novitatem (novedad)
- Ad numerum / ad populum (mayoría)
- Ad odium (odio)
- Ad verecundiam (autoridad)
- Ad superbiam (orgullo)

IMPORTANTE:
- Son solo indicios, no pruebas “fuertes”.
- Pueden dar falsos positivos / negativos.
- Se usan como variable exploratoria para matizar el análisis.
"""

from __future__ import annotations
from typing import Dict, Any, List
import re


FalacyKey = str  # usamos str para poder combinar varias de forma flexible


def _match_any(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE | re.DOTALL) for p in patterns)


# --- Patrones por tipo de falacia -----------------------------------------

PATTERNS_AD_ANTIQUITATEM = [
    r"\bsiempre se ha (hecho|dicho) as[ií]\b",
    r"\bse ha hecho as[ií] toda la vida\b",
    r"\bde toda la vida\b",
    r"\bes nuestra tradici[oó]n\b",
    r"\b(as[ií] ha sido )?siempre\b .* (ser[aá]|ser[íi]a) as[ií]",
]

PATTERNS_AD_BACULUM = [
    r"\bsi no\b.*\bhabr[aá] consecuencias\b",
    r"\bsi no\b.*\bte atienes a las consecuencias\b",
    r"\batente a las consecuencias\b",
    r"\bha(ber[aá]|br[áa]) (castigo|represalias)\b",
    r"\bvais a pagar\b",
]

PATTERNS_AD_CONSEQUENTIAM = [
    r"\bser[ií]a terrible que\b",
    r"\bno podemos permitir que\b",
    r"\b(imagina|imaginen) que\b",
    r"\bsi pasa\b.*\bser[aá] (un desastre|el caos|la ruina)\b",
    r"\bsi\b.*\b(entonces|acabar[ée]mos)\b",
]

PATTERNS_AD_CRUMENAM = [
    r"\bporque (tiene|tienen|ten[eé]is) dinero\b",
    r"\bhabla(n)? as[ií] porque son ricos\b",
    r"\b(el|su) dinero le da la raz[oó]n\b",
    r"\b(el|la|los|las) ricos? tiene(n)? raz[oó]n\b",
]

# Simplificamos: ad hominem / ad personam muy cercanos
INSULT_BASE = r"(imb[eé]cil|idiot[ao]s?|gilipollas|payas[ao]s?|escoria|basura|corrupt[oa]s?)"

PATTERNS_AD_HOMINEM = [
    rf"\b{INSULT_BASE}\b",
    r"\b(vaya|menudo|menuda)\s+(sujeto|tip[oa]|personaje)\b",
    r"\bno me importa el argumento, t[úu] eres\b",
    r"\b(cállate|callaos|cierra la boca)\b",

    # Nuevos: acusaciones morales directas a “ellos”
    r"\b(ellos|esos|esas)\s+ni\s+robar[aá]n?\s+el\s+dinero\s+de\s+los\s+parados\b",
    r"\b(ellos|esos|esas)\s+no\s+robar[aá]n?\b",
]


PATTERNS_AD_PERSONAM = [
    r"\bpor ser (mujer|hombre|joven|viejo|andaluz|catal[aá]n|vasco)\b",
    r"\bno puede hablar alguien\b.*\bque viste as[ií]\b",
    r"\bcon esa (cara|pinta) no\b",
]

PATTERNS_AD_IGNORANTIAM = [
    r"\bnadie ha demostrado lo contrario\b",
    r"\bno hay pruebas de que no\b",
    r"\bcomo no se ha demostrado\b",
    r"\bes verdad porque no se ha probado que sea mentira\b",
]

PATTERNS_AD_LAZARUM = [
    # Pobreza / precariedad como fuente de verdad o legitimidad
    r"\b(pobres?|parados?|desemplead[oa]s?)\b.*\b(tenemos|ten[eé]is|tienen)\s+raz[oó]n\b",
    r"\b(el|los)\s+(pobres|parados|desemplead[oa]s?)\s+no mienten\b",

    # Caso específico del ejemplo: “dinero de los parados”
    r"\bdinero\s+de\s+los\s+parados\b",
]


PATTERNS_AD_LOGICAM = [
    r"\btu argumento es una mierda, as[ií] que est[aá]s equivocado\b",
    r"\bcomo te has explicado mal, no tienes raz[oó]n\b",
    r"\bsolo porque tu l[oó]gica es mala\b.*\best[aá]s equivocado\b",
]

PATTERNS_AD_MISERICORDIAM = [
    r"\bpiensa en (los niñ[oa]s|las v[ií]ctimas|los abuelos)\b",
    r"\bpor pena deber[ií]as\b",
    r"\bda l[aá]stima\b.*\b(as[ií] que|por eso)\b",
    r"\b(no puedes|no debemos) negarles\b.*\bporque sufren\b",
]

PATTERNS_AD_NAUSEAM = [
    r"\blo he dicho mil veces\b",
    r"\buna y otra vez\b",
    r"\bno nos cansaremos de repetir\b",
    r"\brepetimos\b.*\b(es as[ií])\b",
]

PATTERNS_AD_NOVITATEM = [
    r"\bes mejor porque es nuevo\b",
    r"\b(lo|esto) nuevo siempre es mejor\b",
    r"\bantiguo = malo\b",
    r"\bviejo\b.*\bno sirve\b",
]

PATTERNS_AD_NUMERUM = [
    r"\bla mayor[ií]a\b.*\bopina\b",
    r"\bmuchos\b.*\bno pueden estar equivocados\b",
    r"\bmillones de\b.*\bno pueden\b",
    r"\btodo el mundo sabe que\b",
]

PATTERNS_AD_ODIUM = [
    # Odio / asco explícito
    r"\bodio\b",
    r"\bdetest[oa]?\b",
    r"\basco\b",
    r"\brepugnante\b",
    r"\bediond[oa]\b",

    # Nuevos: odio hacia grupos abstractos
    r"\boligarqu[ií]as?\s+globalistas?\s+y\s+corruptas?\b",
    r"\boligarqu[ií]as?\s+globalistas?\b",
    r"\b(elites?|élites?)\s+(globalistas?|corruptas?)\b",

    # Nuevos: metáfora de vendidos / traidores
    r"\b(se vender[aá]n?|se venden|vend[eí]s?|vendisteis)\s+por un plato de gambas\b",
    r"\b(vendidos?|traidores?)\b.*\bplato de gambas\b",
]


PATTERNS_AD_POPULUM = [
    # Apelaciones clásicas a “la gente” / mayoría
    r"\bla gente piensa\b",
    r"\btodo el mundo sabe\b",
    r"\bla mayor[ií]a\b",
    r"\btodos\b.*\bsaben\b",
    r"\btodos\b.*\bpiensan\b",
    r"\bno puede estar equivocada tanta gente\b",

    # Nuevos: patriotismo como criterio de legitimidad
    r"\bcar[aá]cter\s+patri[oó]tico\b",
    r"\b(sindicato|partido|movimiento)\s+nacional\b.*\bpatri[oó]tico\b",
    r"\bverdaderos?\s+patriotas?\b",
    r"\b(la|el)\s+patria\b.*\b(primero|antes que todo)\b",
]


PATTERNS_AD_VERECUNDIAM = [
    r"\bseg[uú]n (los|las) expertos\b",
    r"\bdice la ciencia\b",
    r"\bcomo dijo\b.*\b(Papa|Papa Francisco|Churchill|Einstein|Ortega y Gasset)\b",
    r"\bla (ONU|OCDE|OMS|UE) dice\b",
]

PATTERNS_AD_SUPERBIAM = [
    r"\b(t[úu]|nosotros) somos mejores que\b",
    r"\blo(s)? mejores espa[nñ]oles\b somos\b",
    r"\bsi te respetas aceptar[aá]s\b",
    r"\bno seas mediocre\b.*\bapoya\b",
]


FALACY_PATTERNS: Dict[FalacyKey, List[str]] = {
    "AD_ANTIQUITATEM": PATTERNS_AD_ANTIQUITATEM,
    "AD_BACULUM": PATTERNS_AD_BACULUM,
    "AD_CONSEQUENTIAM": PATTERNS_AD_CONSEQUENTIAM,
    "AD_CRUMENAM": PATTERNS_AD_CRUMENAM,
    "AD_HOMINEM": PATTERNS_AD_HOMINEM,
    "AD_PERSONAM": PATTERNS_AD_PERSONAM,
    "AD_IGNORANTIAM": PATTERNS_AD_IGNORANTIAM,
    "AD_LAZARUM": PATTERNS_AD_LAZARUM,
    "AD_LOGICAM": PATTERNS_AD_LOGICAM,
    "AD_MISERICORDIAM": PATTERNS_AD_MISERICORDIAM,
    "AD_NAUSEAM": PATTERNS_AD_NAUSEAM,
    "AD_NOVITATEM": PATTERNS_AD_NOVITATEM,
    "AD_NUMERUM": PATTERNS_AD_NUMERUM,
    "AD_ODIUM": PATTERNS_AD_ODIUM,
    "AD_POPULUM": PATTERNS_AD_POPULUM,
    "AD_VERECUNDIAM": PATTERNS_AD_VERECUNDIAM,
    "AD_SUPERBIAM": PATTERNS_AD_SUPERBIAM,
}


def detect_fallacies(text: str) -> Dict[str, Any]:
    """
    Devuelve un diccionario con:
    - has_fallacy: True/False (si se detecta al menos una)
    - fallacies_list: lista de etiquetas detectadas (posiblemente varias)
    - fallacies_str: mismas etiquetas pero en un string separado por ';'
    - columnas binarias por cada falacia: AD_ANTIQUITATEM, AD_BACULUM, etc.
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    t = text.strip()
    t_lower = t.lower()

    flags: Dict[str, bool] = {}
    found: List[str] = []

    for key, patterns in FALACY_PATTERNS.items():
        match = _match_any(patterns, t_lower)
        flags[key] = match
        if match:
            found.append(key)

    has_any = len(found) > 0

    result: Dict[str, Any] = {
        "has_fallacy": has_any,
        "fallacies_list": found,
        "fallacies_str": ";".join(found) if found else "",
    }

    # Añadimos las columnas binarias por tipo
    result.update(flags)

    return result
