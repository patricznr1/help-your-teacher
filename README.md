# Help Your Teacher

MSIT Codio assignment - interactive student grade manager in Python.

## Run

```
python3 main.py
```

The program asks for each student in turn:

1. Student name
2. A grade for each subject in ``SUBJECTS`` (default: English, Math, Science)
3. After saving the student, asks whether to add another

When you're done it prints, for every student: best grade, average grade,
and the per-subject breakdown.

It then prints the two bonus reports:

- **Average grades per subject** (one line per subject) plus the
  **overall average across all subjects**
- **Failing grades** (any grade strictly below ``PASSING_GRADE``,
  default 4.0)

## Public functions

`main.py` (also re-exported from `students.py`):

- `get_grade(subject)` - prompt for one grade, retry on invalid input
- `get_student_info(subjects=SUBJECTS)` - collect name + all grades for one student
- `collect_students(subjects=SUBJECTS)` - loop over the above
- `best_grade(student)` / `average_grade(student)` - per-student helpers
- `calculate_average_grades(students)` - bonus: (per-subject dict, overall)
- `calculate_failing_grades(students, threshold=4.0)` - bonus: list of (name, subject, grade)
- `print_student_info(student)` - human-readable single-student summary

## Bonus

See [`bonus_alternative_structures.md`](./bonus_alternative_structures.md)
for a write-up on the nested ``list[dict] -> dict[subject, grade]`` shape
the assignment uses and three alternatives (dict-of-dicts, pandas
DataFrame, dataclasses) with trade-offs.
