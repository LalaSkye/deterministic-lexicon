# deterministic-lexicon

A tiny, deterministic vocabulary primitive. Fixed terms, exact matches, no inference.

**v0.1.0** | MIT License | Zero dependencies

## What it does

`DeterministicLexicon` stores a fixed set of `{term: definition}` pairs. After construction, the lexicon is frozen (immutable). All lookups are exact-match, O(1), with no fallbacks and no fuzzy matching.

## Quickstart

```python
from deterministic_lexicon import DeterministicLexicon

lex = DeterministicLexicon({
    "ALLOW": "Permission to proceed",
    "DENY": "Permission refused",
    "HOLD": "Awaiting further input",
    "HALT": "Immediate stop",
})

# Check if a term exists
lex.has("ALLOW")        # True
lex.has("UNKNOWN")      # False

# Get a definition
lex.get("ALLOW")        # "Permission to proceed"

# Validate and normalise a term
lex.validate(" ALLOW ") # "ALLOW" (stripped)

# Whitespace is stripped automatically
lex.get(" DENY ")       # "Permission refused"

# Unknown terms raise KeyError
lex.get("NOPE")         # KeyError: 'NOPE'

# Bad input raises ValueError
lex.has("")             # ValueError
lex.has(None)           # ValueError
```

## API

| Method | Returns | Raises |
|---|---|---|
| `has(term)` | `bool` | `ValueError` (bad input) |
| `get(term)` | `str` (definition) | `ValueError`, `KeyError` |
| `validate(term)` | `str` (normalised term) | `ValueError`, `KeyError` |
| `keys()` | all terms | - |
| `values()` | all definitions | - |
| `items()` | `(term, definition)` pairs | - |

## Construction rules

- Input must be `dict[str, str]`
- All keys and values are stripped of whitespace
- Empty or whitespace-only keys/values are rejected (`ValueError`)
- Strip-collisions (e.g. `"ALLOW"` and `" ALLOW "`) are rejected (`ValueError`)
- After construction, the lexicon is frozen via `MappingProxyType` (no mutation)

## Run tests

```bash
pip install pytest
python -m pytest test_deterministic_lexicon.py -v
```

## Constraints

- ~100 LOC (implementation only)
- Zero dependencies (stdlib only)
- Read-only after construction
- No fallbacks, no fuzzy matching, no inference
- All operations are O(1) dict lookups
- Deterministic: same inputs always produce same outputs
- No global state, no state leakage between instances
