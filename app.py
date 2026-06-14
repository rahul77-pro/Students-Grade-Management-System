from __future__ import annotations


class StudentGradeManager:
    def __init__(self) -> None:
        self._students: dict[str, list[float]] = {}

    def add_student(self, name: str) -> bool:
        normalized_name = name.strip()
        if not normalized_name or normalized_name in self._students:
            return False
        self._students[normalized_name] = []
        return True

    def add_grade(self, name: str, grade: float) -> bool:
        normalized_name = name.strip()
        if normalized_name not in self._students or grade < 0 or grade > 100:
            return False
        self._students[normalized_name].append(grade)
        return True

    def get_average(self, name: str) -> float | None:
        grades = self._students.get(name.strip())
        if grades is None:
            return None
        if not grades:
            return 0.0
        return sum(grades) / len(grades)

    def report(self) -> dict[str, float]:
        return {name: self.get_average(name) or 0.0 for name in sorted(self._students)}


def main() -> None:
    manager = StudentGradeManager()

    while True:
        print("\nStudent Grade Management System")
        print("1. Add student")
        print("2. Add grade")
        print("3. View report")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Student name: ").strip()
            if manager.add_student(name):
                print(f"Added student '{name}'.")
            else:
                print("Could not add student. Name may be empty or already exists.")
        elif choice == "2":
            name = input("Student name: ").strip()
            grade_input = input("Grade (0-100): ").strip()
            try:
                grade = float(grade_input)
            except ValueError:
                print("Invalid grade format.")
                continue

            if manager.add_grade(name, grade):
                print(f"Added grade {grade:.2f} for '{name}'.")
            else:
                print("Could not add grade. Check student name and grade range.")
        elif choice == "3":
            report = manager.report()
            if not report:
                print("No students available.")
                continue

            print("\nAverage Grades")
            print("-" * 20)
            for student_name, average in report.items():
                print(f"{student_name}: {average:.2f}")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
