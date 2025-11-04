import os
import click

class Professor:
    def __init__(self):
        self.file_path = "professor.csv"

    def read_data(self):
        data = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        email, professor_name, rank, course_id = line.split(",")
                        data[professor_name] = {
                            "email": email,
                            "rank": rank,
                            "course_id": course_id
                        }
                    except ValueError as e:
                        click.echo(f"Warning: Skipping malformed line in {self.file_path}: {line}")
                        continue
        return data

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            for professor_name, info in data.items():
                file.write(f"{info['email']},{professor_name},{info['rank']},{info['course_id']}\n")

    def validate_not_null(self, value, field_name):
        if not value or value.strip() == "":
            click.echo(f"Error: {field_name} cannot be empty.")
            return False
        return True

    def validate_unique_email(self, email, exclude_name=None):
        professors = self.read_data()
        for name, info in professors.items():
            if name != exclude_name and info['email'] == email:
                click.echo(f"Error: Email {email} already exists.")
                return False
        return True

    def add_new_professor(self):
        professors = self.read_data()
        click.echo("Please provide the following details to add a new professor:")
        professor_name = click.prompt("Professor Name")

        if not self.validate_not_null(professor_name, "Professor Name"):
            return

        if professor_name in professors:
            click.echo("Professor already exists.")
            return
        
        email = click.prompt("Email")
        if not self.validate_not_null(email, "Email"):
            return
        if not self.validate_unique_email(email):
            return

        rank = click.prompt("Rank")
        course_id = click.prompt("Course ID")
        if not self.validate_not_null(course_id, "Course ID"):
            return

        professors[professor_name] = {
            "email": email,
            "rank": rank,
            "course_id": course_id
        }
        self.write_data(professors)
        click.echo("The new professor record has been added.")
        self.get_professor_details(professor_name)

    def modify_professor_details(self, professor_name, email=None, rank=None, course_id=None):
        professors = self.read_data()

        if professor_name not in professors:
            click.echo("Professor not found.")
            return

        click.echo("Please choose which details to modify.")
        click.echo("1. Email")
        click.echo("2. Rank")
        click.echo("3. Course ID")
        
        try:
            choice = click.prompt("Enter your choice (1-3)", type=int)
            if choice == 1:
                email = click.prompt("Please enter new Email")
                if not self.validate_not_null(email, "Email"):
                    return
                if not self.validate_unique_email(email, exclude_name=professor_name):
                    return
            elif choice == 2:
                rank = click.prompt("Please enter new Rank")
            elif choice == 3:
                course_id = click.prompt("Please enter new Course ID")
                if not self.validate_not_null(course_id, "Course ID"):
                    return
            else:
                click.echo("Invalid choice.")
                return
        except ValueError:
            click.echo("Invalid input. Please enter a number.")
            return

        if email:
            professors[professor_name]["email"] = email
        if rank:
            professors[professor_name]["rank"] = rank
        if course_id:
            professors[professor_name]["course_id"] = course_id

        self.write_data(professors)
        click.echo("Professor information modified successfully")
        click.echo("The updated information for {} is:".format(professor_name))
        self.get_professor_details(professor_name)

    def delete_professor(self, professor_name):
        professors = self.read_data()

        if professor_name not in professors:
            click.echo("Professor not found.")
            return

        del professors[professor_name]
        self.write_data(professors)
        click.echo("Professor deleted successfully")

    def get_professor_details(self, professor_name):
        professors = self.read_data()

        if professor_name not in professors:
            click.echo("Professor not found.")
            return

        info = professors[professor_name]
        click.echo(f"Professor Name: {professor_name}, Email: {info['email']}, Rank: {info['rank']}, Course ID: {info['course_id']}")

    def generate_professor_wise_report(self, professor_name):
        professors = self.read_data()

        if professor_name not in professors:
            click.echo("Professor not found.")
            return

        prof_info = professors[professor_name]
        course_id = prof_info['course_id']

        click.echo("\n" + "=" * 80)
        click.echo(f"PROFESSOR REPORT: {professor_name}")
        click.echo("=" * 80)
        click.echo(f"Email: {prof_info['email']}")
        click.echo(f"Rank: {prof_info['rank']}")
        click.echo(f"Course ID: {course_id}")
        click.echo("\nStudents in this course:")
        click.echo("-" * 80)

        from student import Student
        student_obj = Student()
        students = student_obj.read_data()

        found_students = False
        for (first_name, last_name), info in students.items():
            if info['course_id'] == course_id:
                found_students = True
                click.echo(f"Name: {first_name} {last_name}")
                click.echo(f"Email: {info['email']}")
                click.echo(f"Grade: {info['grade']}, Mark: {info['mark']}")
                click.echo("-" * 80)

        if not found_students:
            click.echo("No students enrolled in this course.")
            click.echo("-" * 80)

        click.echo("=" * 80)