from math import isfinite


PASSING_GRADE = 60
HONOR_ROLL_GRADE = 90


def validate_grade(grade: int | float) -> float:
    if isinstance(grade, bool) or not isinstance(grade, (int, float)):
        raise TypeError("A grade must be a number.")
    if not 0 <= grade <= 100 or not isfinite(grade):
        raise ValueError("A grade must be between 0 and 100.")
    return float(grade)


class Student:
    def __init__(self, student_id: str, name: str) -> None:
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")

        self.student_id = student_id.strip()
        self.name = name.strip()
        self.grades: list[float] = []

    def add_grade(self, grade: int | float) -> None:
        self.grades.append(validate_grade(grade))

    def calculate_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    @property
    def letter_grade(self) -> str:
        average = self.calculate_average()
        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= PASSING_GRADE:
            return "D"
        return "F"

    @property
    def passed(self) -> bool:
        return self.calculate_average() >= PASSING_GRADE

    @property
    def honor_roll(self) -> bool:
        return self.calculate_average() >= HONOR_ROLL_GRADE

    def remove_grade_by_value(self, grade: int | float) -> None:
        grade_to_remove = validate_grade(grade)
        try:
            self.grades.remove(grade_to_remove)
        except ValueError as error:
            message = f"Grade {grade_to_remove:g} was not found."
            raise ValueError(message) from error

    def delete_grade(self, index: int) -> None:
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Grade index must be an integer.")
        if not 0 <= index < len(self.grades):
            raise IndexError("Grade index is out of range.")
        del self.grades[index]

    def report(self) -> str:
        return "\n".join(
            (
                f"Student ID: {self.student_id}",
                f"Student Name: {self.name}",
                f"Number of Grades: {len(self.grades)}",
                f"Average Grade: {self.calculate_average():.2f}",
                f"Letter Grade: {self.letter_grade}",
                f"Pass/Fail: {'Passed' if self.passed else 'Failed'}",
                f"Honor Roll: {self.honor_roll}",
            )
        )


def main() -> None:
    students: dict[str, Student] = {}

    while True:
        print("\nStudent Grade Management")
        print("1. Add student")
        print("2. Add grade")
        print("3. Remove grade")
        print("4. Show student reports")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            return
        if choice == "1":
            student_id = input("Student ID: ").strip()
            name = input("Student name: ").strip()
            try:
                student = Student(student_id, name)
                if student_id in students:
                    message = f"Student ID '{student_id}' already exists."
                    raise ValueError(message)
                students[student_id] = student
                print(f"Student '{name}' added.")
            except ValueError as error:
                print(f"Error: {error}")
            continue

        if choice == "2":
            student = students.get(input("Student ID: ").strip())
            if student is None:
                print("Error: Student ID was not found.")
                continue
            try:
                grade = float(input("Grade (0-100): ").strip())
                student.add_grade(grade)
                print("Grade added.")
            except (TypeError, ValueError) as error:
                print(f"Error: {error}")
            continue

        if choice == "3":
            student = students.get(input("Student ID: ").strip())
            if student is None:
                print("Error: Student ID was not found.")
                continue
            removal_method = (
                input("Remove by value or index? (v/i): ").strip().lower()
            )
            try:
                if removal_method == "v":
                    grade = float(input("Grade value to remove: ").strip())
                    student.remove_grade_by_value(grade)
                elif removal_method == "i":
                    prompt = "Grade number to remove (starting at 1): "
                    grade_index = int(input(prompt).strip())
                    student.delete_grade(grade_index - 1)
                else:
                    message = (
                        "Choose 'v' to remove by value "
                        "or 'i' to remove by index."
                    )
                    raise ValueError(message)
                print("Grade removed.")
            except (TypeError, ValueError, IndexError) as error:
                print(f"Error: {error}")
            continue

        if choice == "4":
            if not students:
                print("No students have been added.")
            else:
                for student in students.values():
                    print(f"\n{student.report()}")
            continue

        print("Error: Choose one of the listed options.")


if __name__ == "__main__":
    main()
