# Help Your Teacher

MSIT Codio assignment - interactive student-grade manager in Python.

## Run

```
python3 students.py
```

The program drops you into a menu:

```
1) Add student
2) Add grades to a student
3) Show one student (name, best, average, all grades)
4) Show class (every student + class average)
5) Quit
```

Grades may be entered comma- or whitespace-separated, e.g. `90, 85 72`.

## Pure helpers

`students.py` still exposes the side-effect-free helpers, so other code or
tests can call them directly:

- `create_student(name, grades=None)`
- `best_grade(student)`
- `average_grade(student)`
- `class_average(students)`
- `print_student(student)`

## Bonus

See [`bonus_alternative_structures.md`](./bonus_alternative_structures.md) for
a write-up on three alternative data structures and their trade-offs
(dict-of-dicts, dataclasses, pandas DataFrame).
