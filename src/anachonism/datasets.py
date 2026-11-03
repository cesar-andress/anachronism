from pathlib import Path
import pandas as pd
from pandas.errors import ParserError


def load_spanish_politicians(
    path: str = "data/raw/tweets_politica_kaggle.csv",
) -> pd.DataFrame:
    """
    Carga el dataset de tweets de políticos españoles.

    Se asume el esquema:
    - cuenta: cuenta (hash) del político
    - partido: partido político
    - timestamp: fecha y hora del tuit (epoch/segundos)
    - tweet: texto del tuit
    """

    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró el fichero {csv_path}. "
            "Asegúrate de haberlo descargado en data/raw/"
        )

    try:
        # Intento 1: separador automático (por si algún día cambias de fichero)
        df = pd.read_csv(
            csv_path,
            sep=None,
            engine="python",
            on_bad_lines="skip",   # saltar líneas mal formadas
        )
    except ParserError:
        print("[AVISO] Error de parseo con separador automático; probando sep='\\t'")
        # Intento 2: forzar tabulación, saltando líneas malas
        df = pd.read_csv(
            csv_path,
            sep="\t",
            engine="python",
            on_bad_lines="skip",   # saltar líneas mal formadas
        )
    except UnicodeDecodeError:
        # Por si hubiera algún problema de codificación
        df = pd.read_csv(
            csv_path,
            sep="\t",
            engine="python",
            encoding="utf-8",
            on_bad_lines="skip",
        )

    # Normalizamos nombres de columnas a minúsculas
    df.columns = [c.lower() for c in df.columns]

    # Comprobamos que estén las columnas esperadas
    for expected in ["cuenta", "partido", "timestamp", "tweet"]:
        if expected not in df.columns:
            print(f"[AVISO] No se ha encontrado la columna '{expected}' en el CSV.")

    return df
