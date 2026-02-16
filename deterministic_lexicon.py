"""deterministic_lexicon.py

A tiny, deterministic vocabulary primitive.
Fixed terms, exact matches, no inference.

v0.1.0
"""

from types import MappingProxyType


class DeterministicLexicon:
    """A frozen, deterministic vocabulary.

    Accepts a dict[str, str] of {term: definition} pairs.
    After construction, the lexicon is immutable.
    All lookups are exact-match, O(1), no fallbacks.
    """

    def __init__(self, terms: dict) -> None:
        """Build lexicon from a dict of {term: definition} pairs.

        Raises ValueError for:
          - Non-dict input
          - Non-string keys or values
          - Empty or whitespace-only keys (after strip)
          - Empty or whitespace-only values (after strip)
          - Strip-collisions (two keys that normalise to the same string)
        """
        if not isinstance(terms, dict):
            raise ValueError("terms must be a dict")

        normalised = {}
        for key, value in terms.items():
            if not isinstance(key, str):
                raise ValueError(f"All keys must be str, got {type(key).__name__}")
            if not isinstance(value, str):
                raise ValueError(f"All values must be str, got {type(value).__name__}")

            stripped_key = key.strip()
            if stripped_key == "":
                raise ValueError("Keys must not be empty or whitespace-only")

            stripped_value = value.strip()
            if stripped_value == "":
                raise ValueError(f"Value for '{stripped_key}' must not be empty or whitespace-only")

            if stripped_key in normalised:
                raise ValueError(
                    f"Strip-collision: '{key}' normalises to '{stripped_key}' "
                    f"which already exists"
                )
            normalised[stripped_key] = stripped_value

        self._terms = MappingProxyType(normalised)

    def has(self, term: str) -> bool:
        """Return True if term exists in the lexicon, False otherwise.

        Raises ValueError for non-string or empty/whitespace-only input.
        """
        self._validate_term_input(term)
        return term.strip() in self._terms

    def get(self, term: str) -> str:
        """Return the definition for the given term.

        Raises ValueError for non-string or empty/whitespace-only input.
        Raises KeyError if the term does not exist.
        """
        self._validate_term_input(term)
        stripped = term.strip()
        if stripped not in self._terms:
            raise KeyError(stripped)
        return self._terms[stripped]

    def validate(self, term: str) -> str:
        """Validate that a term exists and return it normalised.

        Raises ValueError for non-string or empty/whitespace-only input.
        Raises KeyError if the term does not exist.
        """
        self._validate_term_input(term)
        stripped = term.strip()
        if stripped not in self._terms:
            raise KeyError(stripped)
        return stripped

    def items(self):
        """Return all (term, definition) pairs."""
        return self._terms.items()

    def keys(self):
        """Return all terms."""
        return self._terms.keys()

    def values(self):
        """Return all definitions."""
        return self._terms.values()

    @staticmethod
    def _validate_term_input(term) -> None:
        """Check that a lookup term is a non-empty string."""
        if not isinstance(term, str):
            raise ValueError(f"Term must be str, got {type(term).__name__}")
        if term.strip() == "":
            raise ValueError("Term must not be empty or whitespace-only")
