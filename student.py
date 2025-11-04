import os
import click
import time

class Student:
    def __init__(self):
        self.file_path = "student.csv"
    
    def mark_to_grade(self, mark):
        """Convert numerical mark to letter grade"""
        try:
            mark_value = float(mark)
            if mark_value >= 93:
                return 'A'
            elif mark_value >= 85:
                return 'B'
            elif mark_value >= 75:
                return 'C'
            elif mark_value >= 60:
                return 'D'
            else:
                return 'F'
        except ValueError:
            return mark  # Return as-is if not a number
    
    def grade_to_mark(self, grade):
        """Convert letter grade to representative numerical mark"""
        grade_map = {
            'A': 96.5,  # Middle of 93-100
            'B': 88.5,  # Middle of 85-92
            'C': 79.5,  # Middle of 75-84
            'D': 67.0,  # Middle of 60-74
            'F': 30.0   # Representative failing grade
        }
        return grade_map.get(grade.upper(), grade)
    
    def get_sortable_mark(self, mark):
        """Convert mark to float for sorting, handling both numbers and letter grades"""
        try:
            return float(mark)
        except ValueError:
            # If it's a letter grade, convert it to numerical value
            return float(self.grade_to_mark(mark))

    def read_data(self):
        students = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        email, first_name, last_name, course_id, grade, mark = line.split(",")
                        key = (first_name, last_name)
                        students[key] = {
                            "email": email,
                            "course_id": course_id,
                            "grade": grade,
                            "mark": mark
                        }
                    except ValueError as e:
                        click.echo(f"Warning: Skipping malformed line in {self.file_path}: {line}")
                        continue
        return students

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            for (first_name, last_name), info in data.items():
                file.write(f"{info['email']},{first_name},{last_name},{info['course_id']},{info['grade']},{info['mark']}\n")

    def validate_not_null(self, value, field_name):
        if not value or value.strip() == "":
            click.echo(f"Error: {field_name} cannot be empty.")
            return False
        return True

    def validate_unique_email(self, email, exclude_key=None):
        students = self.read_data()
        for key, info in students.items():
            if key != exclude_key and info['email'] == email:
                click.echo(f"Error: Email {email} already exists.")
                return False
        return True

    def add_new_student(self):
        students = self.read_data()
        click.echo("Please provide the following details to add a new student:")
        first_name = click.prompt("First Name")
        last_name = click.prompt("Last Name")

        if not self.validate_not_null(first_name, "First Name"):
            return
        if not self.validate_not_null(last_name, "Last Name"):
            return

        key = (first_name, last_name)

        if key in students:
            click.echo("Student already exists.")
            return
        
        email = click.prompt("Email")
        if not self.validate_not_null(email, "Email"):
            return
        if not self.validate_unique_email(email):
            return

        course_id = click.prompt("Course ID")
        if not self.validate_not_null(course_id, "Course ID"):
            return

        # Ask user if they want to enter grade or mark
        click.echo("\nHow would you like to enter the grade?")
        click.echo("1. Enter numerical mark (0-100) - grade will be calculated automatically")
        click.echo("2. Enter letter grade (A, B, C, D, F) - representative mark will be assigned")
        
        try:
            choice = click.prompt("Enter your choice (1-2)", type=int)
        except ValueError:
            click.echo("Invalid input.")
            return
        
        if choice == 1:
            mark = click.prompt("Mark (0-100)")
            try:
                mark_value = float(mark)
                if mark_value < 0 or mark_value > 100:
                    click.echo("Error: Mark must be between 0 and 100.")
                    return
                grade = self.mark_to_grade(mark)
                click.echo(f"Automatically assigned grade: {grade}")
            except ValueError:
                click.echo("Error: Mark must be a number.")
                return
        elif choice == 2:
            grade = click.prompt("Grade (A/B/C/D/F)").upper()
            if grade not in ['A', 'B', 'C', 'D', 'F']:
                click.echo("Error: Grade must be A, B, C, D, or F.")
                return
            mark = str(self.grade_to_mark(grade))
            click.echo(f"Automatically assigned mark: {mark}")
        else:
            click.echo("Invalid choice.")
            return

        students[key] = {
            "email": email,
            "course_id": course_id,
            "grade": grade,
            "mark": mark
        }
        self.write_data(students)
        click.echo("The new student record has been added.")
        self.get_student_details(first_name, last_name)

    def modify_student_details(self, first_name, last_name, email=None, course_id=None, grade=None, mark=None):
        students = self.read_data()
        key = (first_name, last_name)

        if key not in students:
            click.echo("Student not found.")
            return
        
        click.echo("Please choose which details to modify.")
        click.echo("1. Email")
        click.echo("2. Course ID")
        click.echo("3. Grade (mark will be updated automatically)")
        click.echo("4. Mark (grade will be updated automatically)")
        
        try:
            choice = click.prompt("Enter your choice (1-4)", type=int)
            if choice == 1:
                email = click.prompt("Please enter new Email")
                if not self.validate_not_null(email, "Email"):
                    return
                if not self.validate_unique_email(email, exclude_key=key):
                    return
                students[key]["email"] = email
            elif choice == 2:
                course_id = click.prompt("Please enter new Course ID")
                if not self.validate_not_null(course_id, "Course ID"):
                    return
                students[key]["course_id"] = course_id
            elif choice == 3:
                grade = click.prompt("Please enter new Grade (A/B/C/D/F)").upper()
                if grade not in ['A', 'B', 'C', 'D', 'F']:
                    click.echo("Error: Grade must be A, B, C, D, or F.")
                    return
                mark = str(self.grade_to_mark(grade))
                students[key]["grade"] = grade
                students[key]["mark"] = mark
                click.echo(f"Grade updated to {grade}, mark automatically updated to {mark}")
            elif choice == 4:
                mark = click.prompt("Please enter new Mark (0-100)")
                try:
                    mark_value = float(mark)
                    if mark_value < 0 or mark_value > 100:
                        click.echo("Error: Mark must be between 0 and 100.")
                        return
                    grade = self.mark_to_grade(mark)
                    students[key]["mark"] = mark
                    students[key]["grade"] = grade
                    click.echo(f"Mark updated to {mark}, grade automatically updated to {grade}")
                except ValueError:
                    click.echo("Error: Mark must be a number.")
                    return
            else:
                click.echo("Invalid choice.")
                return
        except ValueError:
            click.echo("Invalid input.")
            return

        self.write_data(students)
        click.echo("Student information modified successfully")
        click.echo("The new information for {} {} is:".format(first_name, last_name))
        self.get_student_details(first_name, last_name)

    def delete_student(self, first_name, last_name):
        students = self.read_data()
        key = (first_name, last_name)

        if key not in students:
            click.echo("Student not found.")
            return

        del students[key]
        self.write_data(students)
        click.echo("Student deleted successfully")
    
    def get_mean_grade(self, course_id):
        students = self.read_data()
        total_points = 0
        count = 0

        for info in students.values():
            if info["course_id"] == course_id:
                try:
                    # Use mark instead of grade for calculation
                    mark_value = self.get_sortable_mark(info["mark"])
                    total_points += mark_value
                    count += 1
                except ValueError:
                    continue

        if count == 0:
            click.echo("No students found for this course.")
            return 0

        mean_grade = total_points / count
        return mean_grade

    def get_median_grade(self, course_id):
        students = self.read_data()
        marks = []

        for info in students.values():
            if info["course_id"] == course_id:
                try:
                    # Use mark instead of grade for calculation
                    mark_value = self.get_sortable_mark(info["mark"])
                    marks.append(mark_value)
                except ValueError:
                    continue

        if not marks:
            click.echo("No students found for this course.")
            return 0

        marks.sort()
        n = len(marks)
        mid = n // 2

        if n % 2 == 0:
            median_grade = (marks[mid - 1] + marks[mid]) / 2
        else:
            median_grade = marks[mid]

        return median_grade

    def get_student_details(self, first_name, last_name):
        students = self.read_data()
        key = (first_name, last_name)

        if key not in students:
            click.echo("Student not found.")
            return

        info = students[key]
        click.echo(f"First Name: {first_name}, Last Name: {last_name}, Email: {info['email']}, "
              f"Course ID: {info['course_id']}, Grade: {info['grade']}, Mark: {info['mark']}")
        
    def sort_students_by_name(self, order='asc'):
        start_time = time.time()
        students = self.read_data()
        
        sorted_students = sorted(
            students.items(),
            key=lambda x: (x[0][1].lower(), x[0][0].lower()),
            reverse=(order == 'desc')
        )
        
        end_time = time.time()
        sort_time = end_time - start_time
        
        click.echo(f"\nStudents sorted by name ({order}ending order):")
        click.echo("-" * 80)
        for (first_name, last_name), info in sorted_students:
            click.echo(f"{last_name}, {first_name} | Email: {info['email']} | "
                    f"Course: {info['course_id']} | Grade: {info['grade']} | Mark: {info['mark']}")
        click.echo("-" * 80)
        click.echo(f"Sort completed in {sort_time:.6f} seconds")
        click.echo(f"Total records: {len(sorted_students)}")
        
        return sorted_students, sort_time

    def sort_students_by_marks(self, order='asc'):
        start_time = time.time()
        students = self.read_data()

        sorted_students = sorted(
            students.items(),
            key=lambda x: self.get_sortable_mark(x[1]['mark']),
            reverse=(order == 'desc')
        )
        
        end_time = time.time()
        sort_time = end_time - start_time
        
        click.echo(f"\nStudents sorted by marks ({order}ending order):")
        click.echo("-" * 80)
        for (first_name, last_name), info in sorted_students:
            click.echo(f"Mark: {info['mark']} | Grade: {info['grade']} | {first_name} {last_name} | "
                    f"Email: {info['email']} | Course: {info['course_id']}")
        click.echo("-" * 80)
        click.echo(f"Sort completed in {sort_time:.6f} seconds")
        click.echo(f"Total records: {len(sorted_students)}")
        
        return sorted_students, sort_time

    def sort_students_by_email(self, order='asc'):
        start_time = time.time()
        students = self.read_data()

        sorted_students = sorted(
            students.items(),
            key=lambda x: x[1]['email'].lower(),
            reverse=(order == 'desc')
        )
        
        end_time = time.time()
        sort_time = end_time - start_time
        
        click.echo(f"\nStudents sorted by email ({order}ending order):")
        click.echo("-" * 80)
        for (first_name, last_name), info in sorted_students:
            click.echo(f"Email: {info['email']} | {first_name} {last_name} | "
                    f"Course: {info['course_id']} | Grade: {info['grade']} | Mark: {info['mark']}")
        click.echo("-" * 80)
        click.echo(f"Sort completed in {sort_time:.6f} seconds")
        click.echo(f"Total records: {len(sorted_students)}")
        
        return sorted_students, sort_time

    def search_student(self, search_term):
        start_time = time.time()
        students = self.read_data()
        results = []
        
        search_term = search_term.lower()
        
        for (first_name, last_name), info in students.items():
            if (search_term in first_name.lower() or 
                search_term in last_name.lower() or 
                search_term in info['email'].lower() or 
                search_term in info['course_id'].lower()):
                
                results.append({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': info['email'],
                    'course_id': info['course_id'],
                    'grade': info['grade'],
                    'mark': info['mark']
                })
        
        end_time = time.time()
        search_time = end_time - start_time
        
        if results:
            click.echo(f"\nFound {len(results)} student(s) matching '{search_term}':")
            click.echo("-" * 80)
            for student in results:
                click.echo(f"Name: {student['first_name']} {student['last_name']}")
                click.echo(f"Email: {student['email']}")
                click.echo(f"Course: {student['course_id']}")
                click.echo(f"Grade: {student['grade']}, Mark: {student['mark']}")
                click.echo("-" * 80)
        else:
            click.echo(f"No students found matching '{search_term}'")
        
        click.echo(f"\nSearch completed in {search_time:.6f} seconds")
        return results, search_time

    def generate_student_wise_report(self, first_name, last_name):
        students = self.read_data()
        key = (first_name, last_name)

        if key not in students:
            click.echo("Student not found.")
            return

        info = students[key]
        click.echo("\n" + "=" * 80)
        click.echo(f"STUDENT REPORT: {first_name} {last_name}")
        click.echo("=" * 80)
        click.echo(f"Email: {info['email']}")
        click.echo(f"Course ID: {info['course_id']}")
        click.echo(f"Grade: {info['grade']}")
        click.echo(f"Mark: {info['mark']}")
        click.echo("=" * 80)