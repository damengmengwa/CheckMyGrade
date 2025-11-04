import os
import click

class Course:
    def __init__(self):
        self.file_path = "course.csv"

    def read_data(self):
        courses = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        course_id, course_name, credits, description = line.split(",")
                        courses[course_id] = {
                            "course_name": course_name,
                            "credits": credits,
                            "description": description
                        }
                    except ValueError as e:
                        click.echo(f"Warning: Skipping malformed line in {self.file_path}: {line}")
                        continue
        return courses

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            for course_id, info in data.items():
                file.write(f"{course_id},{info['course_name']},{info['credits']},{info['description']}\n")

    def validate_not_null(self, value, field_name):
        if not value or value.strip() == "":
            click.echo(f"Error: {field_name} cannot be empty.")
            return False
        return True

    def add_new_course(self):
        courses = self.read_data()
        click.echo("Please provide the following details to add a new course:")
        course_id = click.prompt("Course ID")

        if not self.validate_not_null(course_id, "Course ID"):
            return

        if course_id in courses:
            click.echo("Course already exists.")
            return
        
        course_name = click.prompt("Course Name")
        if not self.validate_not_null(course_name, "Course Name"):
            return

        credits = click.prompt("Credits")
        description = click.prompt("Description")

        courses[course_id] = {
            "course_name": course_name,
            "credits": credits,
            "description": description
        }
        self.write_data(courses)
        click.echo("The new course record has been added.")
        self.print_course_details(course_id)

    def modify_course_details(self):
        click.echo("Please provide the following details to modify a course:")
        course_id = click.prompt("Course ID")

        courses = self.read_data()

        if course_id not in courses:
            click.echo("Course not found.")
            return

        course_name = click.prompt("Course Name", default=courses[course_id]["course_name"], show_default=True)
        credits = click.prompt("Credits", default=courses[course_id]["credits"], show_default=True)
        description = click.prompt("Description", default=courses[course_id]["description"], show_default=True)

        if not self.validate_not_null(course_name, "Course Name"):
            return

        courses[course_id] = {
            "course_name": course_name,
            "credits": credits,
            "description": description
        }
        self.write_data(courses)
        click.echo("Course information modified successfully.")
        self.print_course_details(course_id)

    def delete_course(self, course_id):
        courses = self.read_data()

        if course_id not in courses:
            click.echo("Course not found")
            return

        del courses[course_id]
        self.write_data(courses)
        click.echo("Course deleted successfully")

    def print_course_details(self, course_id):
        courses = self.read_data()

        if course_id not in courses:
            click.echo("Course not found.")
            return

        info = courses[course_id]
        click.echo(f"Course ID: {course_id}, Course Name: {info['course_name']}, Credits: {info['credits']}, Description: {info['description']}")

    def generate_course_wise_report(self, course_id):
        courses = self.read_data()

        if course_id not in courses:
            click.echo("Course not found.")
            return

        course_info = courses[course_id]

        click.echo("\n" + "=" * 80)
        click.echo(f"COURSE REPORT: {course_id}")
        click.echo("=" * 80)
        click.echo(f"Course Name: {course_info['course_name']}")
        click.echo(f"Credits: {course_info['credits']}")
        click.echo(f"Description: {course_info['description']}")

        from professor import Professor
        professor_obj = Professor()
        professors = professor_obj.read_data()
        professor_name = None
        for name, info in professors.items():
            if info['course_id'] == course_id:
                professor_name = name
                break

        if professor_name:
            click.echo(f"Professor: {professor_name}")
        else:
            click.echo("Professor: Not assigned")

        click.echo("\nEnrolled Students:")
        click.echo("-" * 80)

        from student import Student
        student_obj = Student()
        students = student_obj.read_data()

        found_students = False
        total_marks = 0
        count = 0

        for (first_name, last_name), info in students.items():
            if info['course_id'] == course_id:
                found_students = True
                click.echo(f"Name: {first_name} {last_name}")
                click.echo(f"Email: {info['email']}")
                click.echo(f"Grade: {info['grade']}, Mark: {info['mark']}")
                click.echo("-" * 80)
                try:
                    total_marks += float(info['mark'])
                    count += 1
                except ValueError:
                    pass

        if not found_students:
            click.echo("No students enrolled in this course.")
            click.echo("-" * 80)
        else:
            avg_mark = total_marks / count if count > 0 else 0
            click.echo(f"Total Students: {count}")
            click.echo(f"Average Mark: {avg_mark:.2f}")

        click.echo("=" * 80)