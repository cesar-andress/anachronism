"""Anachonism offline analysis package (rule-based heuristics).

These modules implement transparent regex/heuristic indicators used in the
academic salvage study. They do NOT provide independently validated
classifications of rhetorical fallacies, discursive anachronisms, or semantic vacuity.
"""

from .label_functions import classify_function
from .fallacies import detect_fallacies
from .h2_semantics import classify_h2
from .h3_vacuity import classify_h3

__version__ = "1.0.2"

__all__ = [
    "__version__",
    "classify_function",
    "detect_fallacies",
    "classify_h2",
    "classify_h3",
]
