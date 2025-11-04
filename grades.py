import os
import click
from professor import Professor

class Grades:
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

    def read_data(self):
        grades = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        email, first_name, last_name, course_id, grade, mark = line.split(",")
                        key = (first_name, last_name, course_id)
                        grades[key] = {
                            "email": email,
                            "grade": grade,
                            "mark": mark
                        }
                    except ValueError as e:
                        click.echo(f"Warning: Skipping malformed line in {self.file_path}: {line}")
                        continue
        return grades

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            for (first_name, last_name, course_id), info in data.items():
                file.write(f"{info['email']},{first_name},{last_name},{course_id},{info['grade']},{info['mark']}\n")

    def add_student_grade(self, first_name, last_name, course_id, email=None, grade=None, mark=None):
        grades = self.read_data()
        key = (first_name, last_name, course_id)

        if key in grades and grades[key]['grade'] is not None:
            click.echo("Student grade already exists.")
            return

        # Check if the student exists in the system
        from student import Student
        student_obj = Student()
        students = student_obj.read_data()
        student_key = (first_name, last_name)
        
        # If student doesn't exist, ask if they want to create student record
        if student_key not in students:
            click.echo(f"\nStudent {first_name} {last_name} not found in the system.")
            create_student = click.prompt("Would you like to create the student record now?", 
                                        type=click.Choice(['yes', 'no'], case_sensitive=False))
            
            if create_student.lower() == 'no':
                click.echo("Grade addition cancelled. Please add the student record first.")
                return
            
            # Create student record
            click.echo("\n--- Creating Student Record ---")
            email = click.prompt("Email")
            
            # Validate email
            if not student_obj.validate_not_null(email, "Email"):
                return
            if not student_obj.validate_unique_email(email):
                return
            
            # Verify course exists
            from course import Course
            course_obj = Course()
            courses = course_obj.read_data()
            
            if course_id not in courses:
                click.echo(f"Course {course_id} not found in the system.")
                click.echo("Please add the course first before adding student records.")
                return
        else:
            # Student exists, get their email
            email = students[student_key]['email']
            
            # Verify course exists
            from course import Course
            course_obj = Course()
            courses = course_obj.read_data()
            
            if course_id not in courses:
                click.echo(f"Course {course_id} not found in the system.")
                click.echo("Please add the course first before adding grades.")
                return
        
        # Check if professor is assigned to this course
        professor_obj = Professor()
        professors = professor_obj.read_data()
        professor_info = next((prof for prof in professors.values() if prof['course_id'] == course_id), None)
        
        if not professor_info:
            click.echo(f"\nWarning: No professor is assigned to course {course_id}.")
            click.echo("You may want to assign a professor to this course first.")
            continue_anyway = click.prompt("Do you want to continue adding the grade anyway?", 
                                          type=click.Choice(['yes', 'no'], case_sensitive=False))
            if continue_anyway.lower() == 'no':
                click.echo("Grade addition cancelled.")
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

        # Save to grades (student.csv)
        grades[key] = {
            "email": email,
            "grade": grade,
            "mark": mark
        }
        self.write_data(grades)
        
        # Also save to student records if new student
        if student_key not in students:
            students[student_key] = {
                "email": email,
                "course_id": course_id,
                "grade": grade,
                "mark": mark
            }
            student_obj.write_data(students)
            click.echo(f"\nStudent record created for {first_name} {last_name}")
        
        click.echo("The new grade record has been added.")
        self.display_grade_report(first_name, last_name, course_id)

    def modify_student_grade(self, first_name, last_name, course_id, email=None, grade=None, mark=None):
        grades = self.read_data()
        key = (first_name, last_name, course_id)

        if key not in grades:
            click.echo("Student or course not found")
            return

        # Show current professor assignment
        professor_obj = Professor()
        professors = professor_obj.read_data()
        current_professor = None
        current_professor_name = None
        
        for prof_name, prof_info in professors.items():
            if prof_info['course_id'] == course_id:
                current_professor = prof_info
                current_professor_name = prof_name
                break
        
        if current_professor:
            click.echo(f"\nCurrent Professor for {course_id}: {current_professor_name}")
        else:
            click.echo(f"\nNo professor currently assigned to {course_id}")
        
        click.echo(f"\nCurrent Grade: {grades[key]['grade']}, Current Mark: {grades[key]['mark']}")
        click.echo("\nWhat would you like to modify?")
        click.echo("1. Grade only (mark will be updated automatically)")
        click.echo("2. Mark only (grade will be updated automatically)")
        click.echo("3. Professor only")
        click.echo("4. Both grade/mark and professor")
        
        try:
            choice = click.prompt("Enter your choice (1-4)", type=int)
        except ValueError:
            click.echo("Invalid input.")
            return
        
        if choice == 1:
            # Modify grade only
            new_grade = click.prompt("Grade (A/B/C/D/F)", default=grades[key]["grade"], show_default=True).upper()
            if new_grade not in ['A', 'B', 'C', 'D', 'F']:
                click.echo("Error: Grade must be A, B, C, D, or F.")
                return
            new_mark = str(self.grade_to_mark(new_grade))
            grades[key]["grade"] = new_grade
            grades[key]["mark"] = new_mark
            click.echo(f"Grade updated to {new_grade}, mark automatically updated to {new_mark}")
            self.write_data(grades)
            
        elif choice == 2:
            # Modify mark only
            new_mark = click.prompt("Mark (0-100)", default=grades[key]["mark"], show_default=True)
            try:
                mark_value = float(new_mark)
                if mark_value < 0 or mark_value > 100:
                    click.echo("Error: Mark must be between 0 and 100.")
                    return
                new_grade = self.mark_to_grade(new_mark)
                grades[key]["mark"] = new_mark
                grades[key]["grade"] = new_grade
                click.echo(f"Mark updated to {new_mark}, grade automatically updated to {new_grade}")
                self.write_data(grades)
            except ValueError:
                click.echo("Error: Mark must be a number.")
                return
            
        elif choice == 3:
            # Modify professor only
            self._modify_professor_assignment(course_id, professors, current_professor_name)
            
        elif choice == 4:
            # Modify both
            click.echo("\nHow would you like to update the grade?")
            click.echo("1. Update numerical mark (grade will be calculated)")
            click.echo("2. Update letter grade (mark will be assigned)")
            
            try:
                sub_choice = click.prompt("Enter your choice (1-2)", type=int)
            except ValueError:
                click.echo("Invalid input.")
                return
            
            if sub_choice == 1:
                new_mark = click.prompt("Mark (0-100)", default=grades[key]["mark"], show_default=True)
                try:
                    mark_value = float(new_mark)
                    if mark_value < 0 or mark_value > 100:
                        click.echo("Error: Mark must be between 0 and 100.")
                        return
                    new_grade = self.mark_to_grade(new_mark)
                    grades[key]["mark"] = new_mark
                    grades[key]["grade"] = new_grade
                    click.echo(f"Mark updated to {new_mark}, grade automatically updated to {new_grade}")
                except ValueError:
                    click.echo("Error: Mark must be a number.")
                    return
            elif sub_choice == 2:
                new_grade = click.prompt("Grade (A/B/C/D/F)", default=grades[key]["grade"], show_default=True).upper()
                if new_grade not in ['A', 'B', 'C', 'D', 'F']:
                    click.echo("Error: Grade must be A, B, C, D, or F.")
                    return
                new_mark = str(self.grade_to_mark(new_grade))
                grades[key]["grade"] = new_grade
                grades[key]["mark"] = new_mark
                click.echo(f"Grade updated to {new_grade}, mark automatically updated to {new_mark}")
            else:
                click.echo("Invalid choice.")
                return
            
            self.write_data(grades)
            self._modify_professor_assignment(course_id, professors, current_professor_name)
            
        else:
            click.echo("Invalid choice.")
            return

        click.echo("\nGrade information modified successfully")
        click.echo(f"The new information for {first_name} {last_name} in course {course_id} is:")
        self.display_grade_report(first_name, last_name, course_id)
    
    def _modify_professor_assignment(self, course_id, professors, current_professor_name):
        """Helper method to modify professor assignment for a course"""
        click.echo("\nAvailable actions:")
        click.echo("1. Assign a different professor")
        click.echo("2. Remove professor assignment")
        
        try:
            action = click.prompt("Enter your choice (1-2)", type=int)
        except ValueError:
            click.echo("Invalid input.")
            return
        
        if action == 1:
            # Show available professors
            click.echo("\nAvailable professors:")
            for prof_name, prof_info in professors.items():
                click.echo(f"  - {prof_name} (Currently teaching: {prof_info['course_id']})")
            
            new_professor_name = click.prompt("\nEnter the professor name to assign")
            
            if new_professor_name not in professors:
                click.echo("Professor not found.")
                return
            
            # Update the new professor's course
            professors[new_professor_name]['course_id'] = course_id
            
            # If there was a previous professor, we might want to unassign them
            if current_professor_name and current_professor_name != new_professor_name:
                unassign = click.prompt(
                    f"Do you want to unassign {current_professor_name} from {course_id}?",
                    type=click.Choice(['yes', 'no'], case_sensitive=False)
                )
                if unassign.lower() == 'yes':
                    professors[current_professor_name]['course_id'] = ""
            
            # Save professor data
            professor_obj = Professor()
            professor_obj.write_data(professors)
            click.echo(f"\n{new_professor_name} has been assigned to {course_id}")
            
        elif action == 2:
            # Remove professor assignment
            if current_professor_name:
                professors[current_professor_name]['course_id'] = ""
                professor_obj = Professor()
                professor_obj.write_data(professors)
                click.echo(f"\n{current_professor_name} has been unassigned from {course_id}")
            else:
                click.echo("No professor is currently assigned to this course.")
        else:
            click.echo("Invalid choice.")

    def delete_student_grade(self, first_name, last_name, course_id):
        grades = self.read_data()
        key = (first_name, last_name, course_id)

        if key not in grades:
            click.echo("Student or course not found")
            return

        del grades[key]
        self.write_data(grades)
        click.echo("Student grade deleted successfully")

    def get_student_grade(self, first_name, last_name, course_id):
        grades = self.read_data()
        key = (first_name, last_name, course_id)

        if key not in grades:
            click.echo("Grade not found.")
            return None

        info = grades[key]

        professor_obj = Professor()
        professors = professor_obj.read_data()
        professor_name = None
        professor_email = None
        
        for name, prof_info in professors.items():
            if prof_info['course_id'] == course_id:
                professor_name = name
                professor_email = prof_info['email']
                break

        return {
            "course": course_id,
            "professor_name": professor_name if professor_name else "Not assigned",
            "professor_email": professor_email if professor_email else "N/A",
            "student": {
                "first_name": first_name,
                "last_name": last_name,
                "email": info['email']
            },
            "grade": {
                "grade": info['grade'],
                "mark": info['mark']
            }
        }

    def display_grade_report(self, first_name, last_name, course_id):
        grade_info = self.get_student_grade(first_name, last_name, course_id)

        if not grade_info:
            return

        click.echo("\n" + "=" * 80)
        click.echo("GRADE REPORT")
        click.echo("=" * 80)
        click.echo(f"Student: {grade_info['student']['first_name']} {grade_info['student']['last_name']}")
        click.echo(f"Email: {grade_info['student']['email']}")
        click.echo(f"Course: {grade_info['course']}")
        click.echo(f"Professor: {grade_info['professor_name']}")
        if grade_info['professor_email'] != "N/A":
            click.echo(f"Professor Email: {grade_info['professor_email']}")
        click.echo(f"Grade: {grade_info['grade']['grade']}")
        click.echo(f"Mark: {grade_info['grade']['mark']}")
        click.echo("=" * 80)