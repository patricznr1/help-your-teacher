"""Help Your Teacher - interactive grade manager (MSIT Codio assignment).

Workflow:
1. get_grade(subject) prompts the user for a grade for one subject
   (retries until a valid number is entered)
2. get_student_info(subjects) collects one student's name and grades
   across every subject in ``subjects``
3. collect_students(subjects) loops over step 2 until the user is done
4. print_student_info(student) shows name + best + average for one student
5. main() ties it all together and also prints the two bonus reports
   (per-subject averages, failing grades).

The students data structure is a list of dictionaries, where each
dictionary has the shape::

    {"name": str, "grades": {subject_name: float, ...}}

i.e. grades is itself a dict keyed by subject. See README and
bonus_alternative_structures.md for a discussion of alternatives.
"""

SUBJECTS = ("English", "Math", "Science")
PASSING_GRADE = 4.0  # grades strictly below this are 'failing'


def get_grade(subject):
    """Prompt the user for a numeric grade for ``subject`` and return it.

    Loops on bad input (non-number, empty) until a valid number is entered.
    """
    while True:
        raw = input(f"Enter grade for {subject}: ").strip()
        if not raw:
            print("  Grade darf nicht leer sein.")
            continue
        try:
            return float(raw) if "." in raw else int(raw)
        except ValueError:
            print(f"  '{raw}' ist keine gueltige Zahl, bitte erneut.")


def get_student_info(subjects=SUBJECTS):
    """Collect one student: name plus a grade for each subject in ``subjects``.

    Returns the student dict ``{"name": str, "grades": {subject: number}}``.
    """
    while True:
        name = input("Student name: ").strip()
        if name:
            break
        print("  Name darf nicht leer sein.")
    grades = {subject: get_grade(subject) for subject in subjects}
    return {"name": name, "grades": grades}


def collect_students(subjects=SUBJECTS):
    """Collect students in a loop until the user answers no to 'another?'.

    Returns the list of student dicts (possibly empty).
    """
    students = []
    while True:
        students.append(get_student_info(subjects))
        again = input("Add another student? (y/n): ").strip().lower()
        if again not in ("y", "yes", "j", "ja"):
            return students


def best_grade(student):
    """Return the highest grade across all subjects for ``student``."""
    if not student["grades"]:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return max(student["grades"].values())


def average_grade(student):
    """Return the average grade across all subjects for ``student``."""
    grades = list(student["grades"].values())
    if not grades:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return sum(grades) / len(grades)


def print_student_info(student):
    """Print name, best grade, average grade, and the per-subject breakdown."""
    print(f"\nStudent: {student['name']}")
    print(f"  Best grade:    {best_grade(student)}")
    print(f"  Average grade: {average_grade(student):.2f}")
    for subject, grade in student["grades"].items():
        print(f"    {subject}: {grade}")


def calculate_average_grades(students):
    """Bonus: per-subject and overall average across all students.

    Returns ``(per_subject: dict, overall: float)``. Subjects with no grades
    at all are excluded from the per-subject dict; ``overall`` is 0.0 for
    an empty class.
    """
    per_subject_sums = {}
    per_subject_counts = {}
    for student in students:
        for subject, grade in student["grades"].items():
            per_subject_sums[subject] = per_subject_sums.get(subject, 0) + grade
            per_subject_counts[subject] = per_subject_counts.get(subject, 0) + 1
    per_subject = {
        subject: per_subject_sums[subject] / per_subject_counts[subject]
        for subject in per_subject_sums
    }
    if per_subject:
        overall = sum(per_subject.values()) / len(per_subject)
    else:
        overall = 0.0
    return per_subject, overall


def calculate_failing_grades(students, threshold=PASSING_GRADE):
    """Bonus: collect all ``(student_name, subject, grade)`` below ``threshold``.

    Lower threshold means stricter pass requirement. For the US 0-100 scale
    callers can pass ``threshold=60``.
    """
    failing = []
    for student in students:
        for subject, grade in student["grades"].items():
            if grade < threshold:
                failing.append((student["name"], subject, grade))
    return failing


def main():
    """Run the full workflow: collect, print, then both bonus reports."""
    print("== Help Your Teacher ==")
    print(f"Subjects: {', '.join(SUBJECTS)}")
    students = collect_students()
    print("\n== Per student ==")
    for student in students:
        print_student_info(student)
    print("\n== Bonus: average grades per subject ==")
    per_subject, overall = calculate_average_grades(students)
    if per_subject:
        print("Average grades per subject:")
        for subject, avg in per_subject.items():
            print(f"{subject}: {avg:.2f}")
        print(f"\nOverall average grade across all subjects: {overall:.2f}")
    else:
        print("(no grades recorded)")
    print(f"\n== Bonus: failing grades (< {PASSING_GRADE}) ==")
    failing = calculate_failing_grades(students)
    if failing:
        for name, subject, grade in failing:
            print(f"  {name} - {subject}: {grade}")
    else:
        print("  none, congratulations!")


if __name__ == "__main__":
    main()
