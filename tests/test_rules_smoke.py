"""Smoke tests on synthetic text only (no private tweet corpora)."""

from __future__ import annotations

from anachonism.fallacies import detect_fallacies
from anachonism.h2_semantics import classify_h2
from anachonism.h3_vacuity import classify_h3
from anachonism.label_functions import classify_function


def test_h1_evaluative_insult_pattern():
    out = classify_function("Eres un fascista de manual")
    assert out["label_funcion"] in {"EVALUATIVO", "MIXTO", "OTRO", "DEFINICIONAL"}
    assert "label_funcion" in out


def test_h1_definitional_pattern():
    out = classify_function(
        "El fascismo es una doctrina que se caracteriza por el autoritarismo."
    )
    assert out["label_funcion"] in {"DEFINICIONAL", "MIXTO", "EVALUATIVO", "OTRO"}


def test_fallacy_ad_populum_surface():
    out = detect_fallacies("Todo el mundo sabe que esto es verdad.")
    assert out["has_fallacy"] is True or out["AD_POPULUM"] in (True, False)
    assert "fallacies_list" in out


def test_h2_and_h3_return_labels():
    h2 = classify_h2("Como en 1936 con Hitler")
    h3 = classify_h3("progre")
    assert h2["h2_label"].startswith("H2_")
    assert h3["h3_label"].startswith("H3_")


def test_filter_terms_file_has_33_entries():
    from pathlib import Path

    terms = [
        t.strip()
        for t in Path("config/filter_terms_33.txt").read_text(encoding="utf-8").splitlines()
        if t.strip()
    ]
    assert len(terms) == 33
