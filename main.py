from professor import Professor
from course import Course
from student import Student
from grades import Grades
import time
import click
from authentication import Authentication

class CheckMyGradeApp:
    def __init__(self):
        self.student = Student()
        self.professor = Professor()
        self.course = Course()
        self.grades = Grades()

    def professor_menu(self):
        while True:
            click.echo("\nProfessor Menu:")
            click.echo("1. Add Student Records")
            click.echo("2. Modify Student Records")
            click.echo("3. Delete Student Records")
            click.echo("4. Add Professor Information")
            click.echo("5. Modify Professor Information")
            click.echo("6. Delete Professor Information")
            click.echo("7. Add Course Information")
            click.echo("8. Modify Course Information")
            click.echo("9. Delete Course Information")
            click.echo("10. Add Grade Record")
            click.echo("11. Modify Grade Record")
            click.echo("12. Delete Grade Record")
            click.echo("13. View Average Grade for a Course")
            click.echo("14. View Median Grade for a Course")
            click.echo("15. Search Student Records")
            click.echo("16. Sort Students by Name")
            click.echo("17. Sort Students by Marks")
            click.echo("18. Sort Students by Email")
            click.echo("19. Generate Course-wise Report")
            click.echo("20. Generate Professor-wise Report")
            click.echo("21. Generate Student-wise Report")
            click.echo("22. Change Password")
            click.echo("23. Exit")

            try:
                choice = input("Enter your choice: ")
            except ValueError:
                click.echo("Invalid input. Please enter a number.")
                continue

            if choice == "1":
                self.student.add_new_student()
            elif choice == "2":
                first_name = click.prompt("Enter student first name")
                last_name = click.prompt("Enter student last name")
                self.student.modify_student_details(first_name, last_name)
            elif choice == "3":
                first_name = click.prompt("Enter student first name to delete")
                last_name = click.prompt("Enter student last name to delete")
                self.student.delete_student(first_name, last_name)
            elif choice == "4":
                self.professor.add_new_professor()
            elif choice == "5":
                professor_name = click.prompt("Enter professor name to modify")
                self.professor.modify_professor_details(professor_name)
            elif choice == "6":
                professor_name = click.prompt("Enter professor name to delete")
                self.professor.delete_professor(professor_name)
            elif choice == "7":
                self.course.add_new_course()
            elif choice == "8":
                self.course.modify_course_details()
            elif choice == "9":
                course_id = click.prompt("Enter course ID to delete")
                self.course.delete_course(course_id)
            elif choice == "10":
                first_name = click.prompt("Enter student first name")
                last_name = click.prompt("Enter student last name")
                course_id = click.prompt("Enter course ID")
                self.grades.add_student_grade(first_name, last_name, course_id)
            elif choice == "11":
                first_name = click.prompt("Enter student first name")
                last_name = click.prompt("Enter student last name")
                course_id = click.prompt("Enter course ID")
                self.grades.modify_student_grade(first_name, last_name, course_id)
            elif choice == "12":
                first_name = click.prompt("Enter student first name")
                last_name = click.prompt("Enter student last name")
                course_id = click.prompt("Enter course ID")
                self.grades.delete_student_grade(first_name, last_name, course_id)
            elif choice == "13":
                course_id = click.prompt("Enter course ID")
                mean = self.student.get_mean_grade(course_id)
                click.echo(f"Average grade for {course_id}: {mean:.2f}")
            elif choice == "14":
                course_id = click.prompt("Enter course ID")
                median = self.student.get_median_grade(course_id)
                click.echo(f"Median grade for {course_id}: {median:.2f}")
            elif choice == "15":
                search_term = click.prompt("Enter search term (name, email, or course ID)")
                self.student.search_student(search_term)
            elif choice == "16":
                order = click.prompt("Enter sort order", type=click.Choice(['asc', 'desc']))
                self.student.sort_students_by_name(order)
            elif choice == "17":
                order = click.prompt("Enter sort order", type=click.Choice(['asc', 'desc']))
                self.student.sort_students_by_marks(order)
            elif choice == "18":
                order = click.prompt("Enter sort order", type=click.Choice(['asc', 'desc']))
                self.student.sort_students_by_email(order)
            elif choice == "19":
                course_id = click.prompt("Enter course ID")
                self.course.generate_course_wise_report(course_id)
            elif choice == "20":
                professor_name = click.prompt("Enter professor name")
                self.professor.generate_professor_wise_report(professor_name)
            elif choice == "21":
                first_name = click.prompt("Enter student first name")
                last_name = click.prompt("Enter student last name")
                self.student.generate_student_wise_report(first_name, last_name)
            elif choice == "22":
                email = click.prompt("Enter your email")
                old_password = click.prompt("Enter old password", hide_input=True)
                new_password = click.prompt("Enter new password", hide_input=True)
                auth = Authentication()
                auth.change_password(email, old_password, new_password)
            elif choice == "23":
                click.echo("Exiting Professor Menu.")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def student_menu(self):
        while True:
            click.echo("\nStudent Menu:")
            click.echo("1. View Personal Grade Information")
            click.echo("2. View Personal Report")
            click.echo("3. Change Password")
            click.echo("4. Exit")

            try:
                choice = input("Enter your choice: ")
            except ValueError:
                click.echo("Invalid input. Please enter a number.")
                continue

            if choice == "1":
                first_name = click.prompt("Enter your first name")
                last_name = click.prompt("Enter your last name")
                self.student.get_student_details(first_name, last_name)
            elif choice == "2":
                first_name = click.prompt("Enter your first name")
                last_name = click.prompt("Enter your last name")
                self.student.generate_student_wise_report(first_name, last_name)
            elif choice == "3":
                email = click.prompt("Enter your email")
                old_password = click.prompt("Enter old password", hide_input=True)
                new_password = click.prompt("Enter new password", hide_input=True)
                auth = Authentication()
                auth.change_password(email, old_password, new_password)
            elif choice == "4":
                click.echo("Exiting Student Menu.")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def welcome_screen(self):
        click.echo("Welcome to CheckMyGrade!")
        time.sleep(1)
        click.echo("Please log in to continue.")

    def create_account(self):
        """Create a new account"""
        auth = Authentication()
        click.echo("\n" + "="*60)
        click.echo("CREATE NEW ACCOUNT")
        click.echo("="*60)
        
        email = click.prompt("Enter your email")
        password = click.prompt("Enter your password", hide_input=True)
        confirm_password = click.prompt("Confirm your password", hide_input=True)
        
        if password != confirm_password:
            click.echo("Error: Passwords do not match. Account creation failed.")
            return False
        
        role = click.prompt("Select your role", 
                          type=click.Choice(['Student', 'Professor'], case_sensitive=False))
        
        auth.create_new_account(email, password, role.capitalize())
        return True

    def login(self):
        auth = Authentication()
        click.echo("\n--- Login ---")
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True)
        role = auth.login(email, password)

        if role:
            click.echo(f"Login successful as {role}")
            return role
        else:
            # Account doesn't exist or wrong password, offer to create account
            create = click.prompt("\nWould you like to create a new account?", 
                                type=click.Choice(['yes', 'no'], case_sensitive=False))
            
            if create.lower() == 'yes':
                if self.create_account():
                    click.echo("\nAccount created successfully! Please login with your new credentials.")
                    return self.login()  # Try to login again with new account
            
            return None

    def main_menu(self):
        self.welcome_screen()
        role = None

        while not role:
            role = self.login()
            if not role:
                exit_choice = click.prompt("\nWould you like to exit the application?", 
                                          type=click.Choice(['yes', 'no'], case_sensitive=False))
                if exit_choice.lower() == 'yes':
                    click.echo("Thank you for using CheckMyGrade. Goodbye!")
                    return

        if role == "Professor":
            self.professor_menu()
        elif role == "Student":
            self.student_menu()
        else:
            click.echo("Unknown role. Exiting.")

def main():
    app = CheckMyGradeApp()
    app.main_menu()

if __name__ == "__main__":
    main()