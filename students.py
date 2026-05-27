"""Help Your Teacher - thin helpers module.

This module re-exports the public functions from ``main`` and provides
two extras (``create_student``, ``class_average``) that work on the same
nested structure used in ``main.py``. They are kept for callers/tests
that want the helpers without invoking the interactive ``main()``.
"""
from main import (
    average_grade,
    best_grade,
    calculate_average_grades,
    calculate_failing_grades,
    get_grade,
    get_student_info,
    print_student_info,
    SUBJECTS,
)


def create_student(name, grades=None):
    """Build a student record with a name and a subject->grade dict."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name muss ein nicht-leerer String sein.")
    grades = dict(grades) if grades else {}
    if not all(isinstance(g, (int, float)) for g in grades.values()):
        raise ValueError("Grades muessen Zahlen sein.")
    return {"name": name.strip(), "grades": grades}


def class_average(students):
    """Return the overall average across the whole class (0.0 if empty)."""
    _per_subject, overall = calculate_average_grades(students)
    return overall


__all__ = [
    "average_grade",
    "best_grade",
    "calculate_average_grades",
    "calculate_failing_grades",
    "class_average",
    "create_student",
    "get_grade",
    "get_student_info",
    "print_student_info",
    "SUBJECTS",
]
