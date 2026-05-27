# Bonus - The students nested structure

The assignment uses **a list of dictionaries**, where each student is
itself a dictionary whose ``grades`` field is **also a dictionary**:

```python
students = [
    {"name": "Alice", "grades": {"English": 4, "Math": 3, "Science": 5}},
    {"name": "Bob",   "grades": {"English": 2, "Math": 5, "Science": 4}},
]
```

That's two levels of nesting: outer **list[dict]** + inner **dict[str, float]**.
Accessing one grade reads ``students[0]["grades"]["English"]``.

## Why this shape is a good fit here

- Heterogeneous subjects per student work naturally (``Bob`` could opt out
  of one subject by omitting that key)
- Iteration is symmetric: outer loop walks students, inner loop walks
  subjects
- It maps 1:1 to JSON, so it can be ``json.dump``-ed without conversion

## Three credible alternatives

### 1. Dict-of-dicts keyed by name

```python
students = {
    "Alice": {"English": 4, "Math": 3, "Science": 5},
    "Bob":   {"English": 2, "Math": 5, "Science": 4},
}
```

The student name moves into the key, eliminating the inner ``"name"`` field
entirely. Looking up a student becomes O(1) and you can't accidentally
store two ``"Alice"`` records.

Trade-off: iteration is over ``.items()`` instead of a plain ``for``, and
renaming a student means re-keying the dict.

### 2. Pandas DataFrame

```python
import pandas as pd
df = pd.DataFrame({
    "name":    ["Alice", "Bob"],
    "English": [4, 2],
    "Math":    [3, 5],
    "Science": [5, 4],
})
df.set_index("name").mean(axis=1)        # per-student average
df.set_index("name").mean(axis=0)        # per-subject average
df[df < 4].stack()                       # failing grades
```

The bonus reports become one-liners. Trade-off: heavy dependency for a
teaching exercise, and missing grades (NaN) need explicit handling.

### 3. List of ``@dataclass`` records

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: dict[str, float] = field(default_factory=dict)

    def average(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0.0
    def best(self):
        return max(self.grades.values()) if self.grades else None
```

Static type-checking with mypy catches ``students[0].nmae`` typos at
edit time, and methods live next to the data they describe. Trade-off:
a bit more ceremony than the dict literal, and JSON serialisation
needs an explicit ``asdict(student)``.

## How we get to the grades

Whichever shape we pick:

| Shape | One student's English grade |
|---|---|
| list[dict] (current) | ``students[0]["grades"]["English"]`` |
| dict[name -> dict] | ``students["Alice"]["English"]`` |
| DataFrame | ``df.loc["Alice", "English"]`` |
| list[Student] (dataclass) | ``students[0].grades["English"]`` |

## TL;DR

For an interactive CLI managing a handful of students per session, the
**list[dict] with a nested grades-dict** (the current shape) is the
right call: cheap to build, easy to print, JSON-friendly. As soon as
unique names + frequent lookup matters, switch to **dict-of-dicts**.
Once you're shipping reports or stats, pandas wins. For long-lived
shared code with multiple maintainers, **dataclasses** for the type
safety.
