![CI](https://github.com/LalaSkye/deterministic-lexicon/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
![stdlib only](https://img.shields.io/badge/stdlib-only-green)
![~100 LOC](https://img.shields.io/badge/LOC-~100-lightgrey)

# deterministic-lexicon

Fixed vocabulary primitive — exact-match lookups, frozen after construction, no inference, no synonyms, no surprises.

**v0.1.0** | MIT License | Zero dependencies

---

## Why This Exists

Systems that rely on natural language parsing or fuzzy matching for control vocabulary introduce ambiguity at the foundation. If your terms drift, everything built on top of them drifts too. This primitive eliminates that: every term is defined once, looked up exactly, and never inferred. If a term is not in the lexicon, it does not exist. Unknown terms are errors, not guesses. This is the foundation layer — authority gates, commit boundaries, and admissibility surfaces all depend on having a stable vocabulary to reason against. Install this primitive before wiring up anything that names control states.

---

## Architecture

```
  ┌────────────────────────────────────────────┐
  │           DeterministicLexicon             │
  │                                            │
  │  Construction:                             │
  │    dict[str, str]  ──> strip + validate    │
  │    strip-collision check                   │
  │    freeze via MappingProxyType             │
  │                                            │
  │  Lookups (O(1), exact match only):         │
  │    has("ALLOW")   --> True / False         │
  │    get("ALLOW")   --> "Permission to proceed"
  │    get("NOPE")    --> KeyError             │
  │    validate(" ALLOW ") --> "ALLOW"         │
  │    has("")        --> ValueError           │
  │                                            │
  │  No fuzzy matching. No synonyms.           │
  │  No inference. No mutation after build.    │
  └────────────────────────────────────────────┘
```

---

## Quickstart

```python
from deterministic_lexicon import DeterministicLexicon

lex = DeterministicLexicon({
    "ALLOW": "Permission to proceed",
    "DENY":  "Permission refused",
    "HOLD":  "Awaiting further input",
    "HALT":  "Immediate stop",
})

# Check existence
lex.has("ALLOW")        # True
lex.has("UNKNOWN")      # False

# Get a definition
lex.get("ALLOW")        # "Permission to proceed"

# Validate and normalise a term (strips whitespace)
lex.validate(" ALLOW ") # "ALLOW"

# Whitespace stripped automatically on all operations
lex.get(" DENY ")       # "Permission refused"

# Unknown terms raise KeyError
lex.get("NOPE")         # KeyError: 'NOPE'

# Bad input raises ValueError
lex.has("")             # ValueError
lex.has(None)           # ValueError

# Iterate
list(lex.keys())        # ["ALLOW", "DENY", "HOLD", "HALT"]
```

---

## API

| Method | Returns | Raises |
|---|---|---|
| `has(term)` | `bool` | `ValueError` (bad input) |
| `get(term)` | `str` (definition) | `ValueError`, `KeyError` |
| `validate(term)` | `str` (normalised term) | `ValueError`, `KeyError` |
| `keys()` | all terms | — |
| `values()` | all definitions | — |
| `items()` | `(term, definition)` pairs | — |

---

## Construction Rules

- Input must be `dict[str, str]`
- All keys and values are stripped of whitespace at construction time
- Empty or whitespace-only keys/values are rejected (`ValueError`)
- Strip-collisions (e.g. `"ALLOW"` and `" ALLOW "`) are rejected (`ValueError`)
- After construction, the lexicon is frozen via `MappingProxyType` — no mutation

---

## Run Tests

```bash
git clone https://github.com/LalaSkye/deterministic-lexicon.git
cd deterministic-lexicon
pip install pytest
python -m pytest test_deterministic_lexicon.py -v
```

Expected output:

```
test_deterministic_lexicon.py::test_has_known_term PASSED
test_deterministic_lexicon.py::test_has_unknown_term PASSED
test_deterministic_lexicon.py::test_get_known_term PASSED
test_deterministic_lexicon.py::test_get_unknown_raises_keyerror PASSED
test_deterministic_lexicon.py::test_validate_strips_whitespace PASSED
test_deterministic_lexicon.py::test_empty_input_raises_valueerror PASSED
test_deterministic_lexicon.py::test_none_input_raises_valueerror PASSED
test_deterministic_lexicon.py::test_frozen_after_construction PASSED
test_deterministic_lexicon.py::test_strip_collision_rejected PASSED
...
```

---

## Constraints

- ~100 LOC (implementation only)
- Zero dependencies (stdlib only)
- Read-only after construction
- No fallbacks, no fuzzy matching, no inference
- All operations are O(1) dict lookups
- Deterministic: same inputs always produce same outputs
- No global state, no state leakage between instances

---

## Part of the Execution Boundary Series

| Repo | Layer | What It Does |
|---|---|---|
| [interpretation-boundary-lab](https://github.com/LalaSkye/interpretation-boundary-lab) | Upstream boundary | 10-rule admissibility gate for interpretations |
| [dual-boundary-admissibility-lab](https://github.com/LalaSkye/dual-boundary-admissibility-lab) | Full corridor | Dual-boundary model with pressure monitoring and C-sector rotation |
| [execution-boundary-lab](https://github.com/LalaSkye/execution-boundary-lab) | Execution boundary | Demonstrates cascading failures without upstream governance |
| [stop-machine](https://github.com/LalaSkye/stop-machine) | Control primitive | Deterministic three-state stop controller |
| [constraint-workshop](https://github.com/LalaSkye/constraint-workshop) | Control primitives | Authority gate, invariant litmus, stop machine |
| [csgr-lab](https://github.com/LalaSkye/csgr-lab) | Measurement | Contracted stability and drift measurement |
| [invariant-lock](https://github.com/LalaSkye/invariant-lock) | Drift prevention | Refuse execution unless version increments |
| [policy-lint](https://github.com/LalaSkye/policy-lint) | Policy validation | Deterministic linter for governance statements |
| [deterministic-lexicon](https://github.com/LalaSkye/deterministic-lexicon) | Vocabulary | Fixed terms, exact matches, no inference |

---

## License

MIT. See `LICENSE`.
