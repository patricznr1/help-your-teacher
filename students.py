"""Help Your Teacher - interactive student grade manager.

The user runs the script and is dropped into a menu loop:
- add a student
- record grades for an existing student
- view best / average grade per student
- view class average
- list all students
- quit

The student records are kept in memory as a list of dictionaries with
the shape ``{"name": str, "grades": list[float]}``. The pure helper
functions (``best_grade``, ``average_grade``, ``class_average``) are
exposed at module level so they remain reusable from other code, e.g.
in tests.
"""
from typing import Optional


def create_student(name, grades=None):
    """Build a fresh student record.

    Args:
        name: Non-empty string.
        grades: Optional list of numbers. Defaults to empty list.

    Raises:
        ValueError: when ``name`` is empty or any grade is not a number.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name muss ein nicht-leerer String sein.")
    grades = list(grades) if grades else []
    if not all(isinstance(g, (int, float)) for g in grades):
        raise ValueError("Grades muss eine Liste von Zahlen sein.")
    return {"name": name.strip(), "grades": grades}


def best_grade(student):
    """Return the highest grade in ``student``'s grade list."""
    if not student["grades"]:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return max(student["grades"])


def average_grade(student):
    """Return the arithmetic mean of ``student``'s grades."""
    if not student["grades"]:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return sum(student["grades"]) / len(student["grades"])


def class_average(students):
    """Return the average of all student averages.

    Students without any grades are skipped. Returns 0.0 for an empty class.
    """
    averages = [average_grade(s) for s in students if s["grades"]]
    if not averages:
        return 0.0
    return sum(averages) / len(averages)


def print_student(student):
    """Print a one-block summary (name, best, average) for ``student``."""
    print(f"Student: {student['name']}")
    if student["grades"]:
        print(f"  Best grade:    {best_grade(student)}")
        print(f"  Average grade: {average_grade(student):.2f}")
        print(f"  Grades:        {student['grades']}")
    else:
        print("  (noch keine Noten erfasst)")


# ---------------------------------------------------------------- interactive

def _find_student(students, name):
    """Return the first student whose name matches ``name`` (case-insensitive)."""
    target = name.strip().lower()
    for student in students:
        if student["name"].lower() == target:
            return student
    return None


def _parse_grades(raw):
    """Parse a comma- or whitespace-separated string of numbers into a list."""
    parts = [p.strip() for p in raw.replace(",", " ").split() if p.strip()]
    grades = []
    for part in parts:
        try:
            grades.append(float(part) if "." in part else int(part))
        except ValueError as exc:
            raise ValueError(f"'{part}' ist keine gueltige Zahl") from exc
    return grades


def _action_add_student(students):
    """Prompt for a student name and add a new record."""
    name = input("Name des Studenten: ").strip()
    if not name:
        print("  Name darf nicht leer sein.")
        return
    if _find_student(students, name):
        print(f"  {name} ist bereits in der Klasse.")
        return
    students.append(create_student(name))
    print(f"  {name} hinzugefuegt.")


def _action_add_grades(students):
    """Prompt for a student name and a list of grades, then append them."""
    if not students:
        print("  Klasse ist leer, erst Studenten hinzufuegen.")
        return
    name = input("Welcher Student? ").strip()
    student = _find_student(students, name)
    if not student:
        print(f"  Kein Student '{name}' gefunden.")
        return
    raw = input("Noten (z.B. '90, 85 72'): ").strip()
    if not raw:
        print("  Keine Noten eingegeben.")
        return
    try:
        new_grades = _parse_grades(raw)
    except ValueError as exc:
        print(f"  Fehler: {exc}")
        return
    student["grades"].extend(new_grades)
    print(f"  {len(new_grades)} Noten zu {student['name']} hinzugefuegt.")


def _action_show_student(students):
    """Prompt for a student name and print that student's summary."""
    if not students:
        print("  Klasse ist leer.")
        return
    name = input("Welcher Student? ").strip()
    student = _find_student(students, name)
    if not student:
        print(f"  Kein Student '{name}' gefunden.")
        return
    print_student(student)


def _action_show_class(students):
    """Print every student plus the class average."""
    if not students:
        print("  Klasse ist leer.")
        return
    for student in students:
        print_student(student)
        print()
    print(f"Class average: {class_average(students):.2f}")


_MENU = """
== Help Your Teacher ==
1) Add student
2) Add grades to a student
3) Show one student
4) Show class (all students + average)
5) Quit
"""


def main():
    """Run the interactive teacher CLI until the user picks Quit."""
    students = []
    actions = {
        "1": _action_add_student,
        "2": _action_add_grades,
        "3": _action_show_student,
        "4": _action_show_class,
    }
    while True:
        print(_MENU)
        choice = input("Choice: ").strip()
        if choice in ("5", "q", "quit", "exit"):
            print("Auf Wiedersehen.")
            return
        action = actions.get(choice)
        if action is None:
            print("  Unbekannte Auswahl.")
            continue
        try:
            action(students)
        except (ValueError, KeyError) as exc:
            print(f"  Fehler: {exc}")


if __name__ == "__main__":
    main()
