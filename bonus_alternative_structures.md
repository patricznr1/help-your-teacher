# Bonus - Alternative nested structures

The assessment uses **a list of dictionaries** to hold students:

```python
[{"name": "Alice", "grades": [90, 85]}, {"name": "Bob", "grades": [70]}]
```

That works, but other shapes are sometimes better. Three credible alternatives:

## 1. Dict-of-dicts keyed by name

```python
{
    "Alice": {"grades": [90, 85]},
    "Bob":   {"grades": [70]},
}
```

**Advantages**
- O(1) lookup by name instead of an O(n) linear scan
- Names are guaranteed unique by construction (no duplicate Alice records)
- Less boilerplate when reading: `students["Alice"]["grades"]`

**Trade-off**
- Iteration order matters less; mixing it with insertion order is fine in Python 3.7+
- The student "owns" their name in the data structure -- if a name has to change, the key has to be moved.

## 2. List of dataclasses (or NamedTuples)

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list[float] = field(default_factory=list)

    def best(self):    return max(self.grades)
    def average(self): return sum(self.grades) / len(self.grades)
```

**Advantages**
- Static type-checking (mypy) catches typos like `student["nmae"]`
- Methods live with the data they describe -- the class itself is documentation
- Equality, repr, and optional immutability come for free

**Trade-off**
- Slightly more setup than a dict literal
- JSON serialisation needs an explicit `asdict(...)`

## 3. Pandas DataFrame (for larger classes)

```python
import pandas as pd
df = pd.DataFrame([
    {"name": "Alice", "grade": 90},
    {"name": "Alice", "grade": 85},
    {"name": "Bob",   "grade": 70},
])
df.groupby("name")["grade"].mean()
```

**Advantages**
- Vectorised group-by means class average is one line
- Easy to add columns later (course, term, weight) without changing function signatures
- Plays well with CSV/Excel import-export

**Trade-off**
- Heavy dependency for a teaching exercise
- Less explicit -- the structure is implicit in column names

## TL;DR

For a tiny in-memory class of a handful of students, **list of dicts** (current code) is fine. Once names need to be unique and looked up often, switch to **dict-of-dicts**. Once the schema starts to grow (extra fields per grade, multiple subjects), reach for **dataclasses** or **pandas**.
