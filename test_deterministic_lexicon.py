"""test_deterministic_lexicon.py

Comprehensive tests for DeterministicLexicon.
Covers all paths, failure modes, and edge cases.
"""

import pytest
from deterministic_lexicon import DeterministicLexicon


# ── Fixtures ──────────────────────────────────────────────

SAMPLE_TERMS = {
    "ALLOW": "Permission to proceed",
    "DENY": "Permission refused",
    "HOLD": "Awaiting further input",
    "HALT": "Immediate stop",
}


@pytest.fixture
def lexicon():
    return DeterministicLexicon(SAMPLE_TERMS)


# ── has() happy paths ────────────────────────────────────

def test_has_known_term(lexicon):
    assert lexicon.has("ALLOW") is True


def test_has_unknown_term(lexicon):
    assert lexicon.has("UNKNOWN") is False


def test_has_strips_whitespace(lexicon):
    assert lexicon.has(" ALLOW ") is True


# ── get() happy paths ────────────────────────────────────

def test_get_known_term(lexicon):
    assert lexicon.get("ALLOW") == "Permission to proceed"


def test_get_strips_whitespace(lexicon):
    assert lexicon.get(" ALLOW ") == "Permission to proceed"


def test_get_unknown_raises_key_error(lexicon):
    with pytest.raises(KeyError):
        lexicon.get("UNKNOWN")


# ── validate() happy paths ───────────────────────────────

def test_validate_known_term(lexicon):
    assert lexicon.validate("DENY") == "DENY"


def test_validate_strips_whitespace(lexicon):
    assert lexicon.validate(" DENY ") == "DENY"


def test_validate_unknown_raises_key_error(lexicon):
    with pytest.raises(KeyError):
        lexicon.validate("NOPE")


# ── Term hygiene (strip + empty + type) ──────────────────

def test_empty_string_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.has("")


def test_whitespace_only_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.has("   ")


def test_none_term_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.has(None)


def test_int_term_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.get(123)


def test_validate_empty_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.validate("")


def test_validate_non_string_raises_value_error(lexicon):
    with pytest.raises(ValueError):
        lexicon.validate(42)


# ── Lexicon hygiene (construction validation) ────────────

def test_non_dict_input_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon("not a dict")


def test_non_string_key_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon({123: "number key"})


def test_non_string_value_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon({"KEY": 456})


def test_empty_key_after_strip_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon({"   ": "whitespace key"})


def test_empty_value_after_strip_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon({"KEY": "   "})


def test_strip_collision_raises_value_error():
    with pytest.raises(ValueError):
        DeterministicLexicon({"ALLOW": "first", " ALLOW ": "second"})


# ── Immutability via MappingProxyType ────────────────────

def test_cannot_assign_to_internal_terms(lexicon):
    with pytest.raises(TypeError):
        lexicon._terms["NEW"] = "injected"


def test_cannot_delete_from_internal_terms(lexicon):
    with pytest.raises(TypeError):
        del lexicon._terms["ALLOW"]


# ── Determinism ──────────────────────────────────────────

def test_same_input_same_output():
    lex1 = DeterministicLexicon(SAMPLE_TERMS)
    lex2 = DeterministicLexicon(SAMPLE_TERMS)
    for term in SAMPLE_TERMS:
        assert lex1.get(term) == lex2.get(term)
        assert lex1.has(term) == lex2.has(term)
        assert lex1.validate(term) == lex2.validate(term)


# ── No state leakage ─────────────────────────────────────

def test_independent_instances_no_leakage():
    lex_a = DeterministicLexicon({"X": "definition of X"})
    lex_b = DeterministicLexicon({"Y": "definition of Y"})
    assert lex_a.has("X") is True
    assert lex_a.has("Y") is False
    assert lex_b.has("Y") is True
    assert lex_b.has("X") is False


# ── items/keys/values ────────────────────────────────────

def test_keys_returns_all_terms(lexicon):
    assert set(lexicon.keys()) == {"ALLOW", "DENY", "HOLD", "HALT"}


def test_values_returns_all_definitions(lexicon):
    vals = set(lexicon.values())
    assert "Permission to proceed" in vals
    assert "Permission refused" in vals


def test_items_returns_pairs(lexicon):
    items = dict(lexicon.items())
    assert items["ALLOW"] == "Permission to proceed"
    assert items["HALT"] == "Immediate stop"
