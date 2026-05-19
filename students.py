"""Help Your Teacher - Student-Dictionary mit Notenberechnung."""


def create_student(name: str, grades: list) -> dict:
    """Erstelle Student-Dict mit Namen und Notenliste."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name muss ein nicht-leerer String sein.")
    if not isinstance(grades, list) or not all(isinstance(g, (int, float)) for g in grades):
        raise ValueError("Grades muss eine Liste von Zahlen sein.")
    return {"name": name, "grades": grades}


def best_grade(student: dict) -> float:
    """Hoechste Note eines Studenten."""
    if not student["grades"]:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return max(student["grades"])


def average_grade(student: dict) -> float:
    """Durchschnittsnote eines Studenten."""
    if not student["grades"]:
        raise ValueError(f"{student['name']} hat keine Noten.")
    return sum(student["grades"]) / len(student["grades"])


def class_average(students: list) -> float:
    """Durchschnittsnote der gesamten Klasse."""
    averages = [average_grade(s) for s in students if s["grades"]]
    if not averages:
        return 0.0
    return sum(averages) / len(averages)


def print_student(student: dict):
    """Drucke Schueler-Info: Name, Beste, Durchschnitt."""
    print(f"Student: {student['name']}")
    print(f"  Best grade: {best_grade(student)}")
    print(f"  Average grade: {average_grade(student):.2f}")


def main():
    """Demo mit Beispiel-Klasse."""
    students = [
        create_student("Alice", [90, 85, 92, 78]),
        create_student("Bob", [70, 75, 80, 65]),
        create_student("Charlie", [100, 95, 98, 92]),
    ]
    for s in students:
        print_student(s)
        print()
    print(f"Class average: {class_average(students):.2f}")


if __name__ == "__main__":
    main()
