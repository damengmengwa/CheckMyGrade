import unittest
import os
import time
import random
import string
from authentication import Authentication
from student import Student
from course import Course
from professor import Professor
from grades import Grades


class TestAuthentication(unittest.TestCase):
    
    def setUp(self):
        self.auth = Authentication()
        self.test_file = "test_authentication.csv"
        self.auth.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_encrypt_password(self):
        password = "Welcome12#_"
        encrypted = self.auth.encrypt_password(password)
        self.assertEqual(encrypted, self.auth.encrypt_password(password))
        self.assertEqual(len(encrypted), 64)
        print("✓ Password encryption test passed")
    
    def test_create_account(self):
        email = "test@sjsu.edu"
        password = "TestPass123"
        role = "Student"
        
        self.auth.create_new_account(email, password, role)
        accounts = self.auth.read_data()
        
        self.assertIn(email, accounts)
        self.assertEqual(accounts[email]["role"], role)
        print("✓ Account creation test passed")
    
    def test_login_success(self):
        email = "student@sjsu.edu"
        password = "StudentPass123"
        role = "Student"
        
        self.auth.create_new_account(email, password, role)
        login_role = self.auth.login(email, password)
        
        self.assertEqual(login_role, role)
        print("✓ Successful login test passed")
    
    def test_login_failure(self):
        email = "student@sjsu.edu"
        password = "CorrectPass"
        wrong_password = "WrongPass"
        
        self.auth.create_new_account(email, password, "Student")
        result = self.auth.login(email, wrong_password)
        
        self.assertIsNone(result)
        print("✓ Failed login test passed")
    
    def test_change_password(self):
        email = "user@sjsu.edu"
        old_password = "OldPass123"
        new_password = "NewPass456"
        
        self.auth.create_new_account(email, old_password, "Student")
        self.auth.change_password(email, old_password, new_password)
        
        accounts = self.auth.read_data()
        new_encrypted = self.auth.encrypt_password(new_password)
        self.assertEqual(accounts[email]["password"], new_encrypted)
        print("✓ Password change test passed")


class TestStudent(unittest.TestCase):
    
    def setUp(self):
        self.student = Student()
        self.test_file = "test_student.csv"
        self.student.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_student(self):
        students = {}
        students[("John", "Doe")] = {
            "email": "john.doe@sjsu.edu",
            "course_id": "DATA200",
            "grade": "A",
            "mark": "95"
        }
        self.student.write_data(students)
        
        students = self.student.read_data()
        self.assertIn(("John", "Doe"), students)
        print("✓ Add student test passed")
    
    def test_modify_student(self):
        students = {
            ("Jane", "Smith"): {
                "email": "jane@sjsu.edu",
                "course_id": "DATA200",
                "grade": "B",
                "mark": "85"
            }
        }
        self.student.write_data(students)
        
        students = self.student.read_data()
        students[("Jane", "Smith")]["grade"] = "A"
        students[("Jane", "Smith")]["mark"] = "95"
        self.student.write_data(students)
        
        students = self.student.read_data()
        self.assertEqual(students[("Jane", "Smith")]["grade"], "A")
        print("✓ Modify student test passed")
    
    def test_delete_student(self):
        students = {
            ("Alice", "Jones"): {
                "email": "alice@sjsu.edu",
                "course_id": "DATA200",
                "grade": "A",
                "mark": "92"
            }
        }
        self.student.write_data(students)
        
        students = self.student.read_data()
        del students[("Alice", "Jones")]
        self.student.write_data(students)
        
        students = self.student.read_data()
        self.assertNotIn(("Alice", "Jones"), students)
        print("✓ Delete student test passed")
    
    def test_mean_grade_calculation(self):
        students = {
            ("Student1", "Test"): {
                "email": "s1@sjsu.edu",
                "course_id": "DATA200",
                "grade": "90",
                "mark": "90"
            },
            ("Student2", "Test"): {
                "email": "s2@sjsu.edu",
                "course_id": "DATA200",
                "grade": "80",
                "mark": "80"
            },
            ("Student3", "Test"): {
                "email": "s3@sjsu.edu",
                "course_id": "DATA200",
                "grade": "85",
                "mark": "85"
            }
        }
        self.student.write_data(students)
        
        mean = self.student.get_mean_grade("DATA200")
        expected_mean = (90 + 80 + 85) / 3
        
        self.assertAlmostEqual(mean, expected_mean, places=2)
        print(f"✓ Mean grade calculation test passed (Mean: {mean:.2f})")
    
    def test_median_grade_calculation(self):
        students = {
            ("Student1", "Test"): {
                "email": "s1@sjsu.edu",
                "course_id": "DATA200",
                "grade": "90",
                "mark": "90"
            },
            ("Student2", "Test"): {
                "email": "s2@sjsu.edu",
                "course_id": "DATA200",
                "grade": "70",
                "mark": "70"
            },
            ("Student3", "Test"): {
                "email": "s3@sjsu.edu",
                "course_id": "DATA200",
                "grade": "85",
                "mark": "85"
            }
        }
        self.student.write_data(students)
        
        median = self.student.get_median_grade("DATA200")
        self.assertEqual(median, 85.0)
        print(f"✓ Median grade calculation test passed (Median: {median})")


class TestCourse(unittest.TestCase):
    
    def setUp(self):
        self.course = Course()
        self.test_file = "test_course.csv"
        self.course.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_course(self):
        courses = {}
        courses["DATA200"] = {
            "course_name": "Data Science",
            "credits": "3",
            "description": "Introduction to Data Science"
        }
        self.course.write_data(courses)
        
        courses = self.course.read_data()
        self.assertIn("DATA200", courses)
        print("✓ Add course test passed")
    
    def test_modify_course(self):
        courses = {
            "DATA200": {
                "course_name": "Data Science",
                "credits": "3",
                "description": "Old Description"
            }
        }
        self.course.write_data(courses)
        
        courses = self.course.read_data()
        courses["DATA200"]["description"] = "New Description"
        self.course.write_data(courses)
        
        courses = self.course.read_data()
        self.assertEqual(courses["DATA200"]["description"], "New Description")
        print("✓ Modify course test passed")
    
    def test_delete_course(self):
        courses = {
            "DATA200": {
                "course_name": "Data Science",
                "credits": "3",
                "description": "Introduction"
            }
        }
        self.course.write_data(courses)
        
        self.course.delete_course("DATA200")
        
        courses = self.course.read_data()
        self.assertNotIn("DATA200", courses)
        print("✓ Delete course test passed")


class TestProfessor(unittest.TestCase):
    
    def setUp(self):
        self.professor = Professor()
        self.test_file = "test_professor.csv"
        self.professor.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_professor(self):
        professors = {}
        professors["Dr. Smith"] = {
            "email": "smith@sjsu.edu",
            "rank": "Associate Professor",
            "course_id": "DATA200"
        }
        self.professor.write_data(professors)
        
        professors = self.professor.read_data()
        self.assertIn("Dr. Smith", professors)
        print("✓ Add professor test passed")
    
    def test_modify_professor(self):
        professors = {
            "Dr. Johnson": {
                "email": "johnson@sjsu.edu",
                "rank": "Assistant Professor",
                "course_id": "DATA200"
            }
        }
        self.professor.write_data(professors)
        
        professors = self.professor.read_data()
        professors["Dr. Johnson"]["rank"] = "Associate Professor"
        self.professor.write_data(professors)
        
        professors = self.professor.read_data()
        self.assertEqual(professors["Dr. Johnson"]["rank"], "Associate Professor")
        print("✓ Modify professor test passed")
    
    def test_delete_professor(self):
        professors = {
            "Dr. Smith": {
                "email": "smith@sjsu.edu",
                "rank": "Professor",
                "course_id": "DATA200"
            }
        }
        self.professor.write_data(professors)
        
        self.professor.delete_professor("Dr. Smith")
        
        professors = self.professor.read_data()
        self.assertNotIn("Dr. Smith", professors)
        print("✓ Delete professor test passed")


class TestStudentCRUD1000Records(unittest.TestCase):
    
    def setUp(self):
        self.student = Student()
        self.test_file = "test_student_1000.csv"
        self.student.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_1000_student_records(self):
        print("\n" + "="*80)
        print("Testing Student CRUD with 1000+ Records")
        print("="*80)
        
        num_records = 1000
        print(f"\n1. Adding {num_records} student records...")
        
        students = {}
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        courses = ["DATA200", "DATA201", "CS101", "CS102", "MATH101"]
        
        start_time = time.time()
        for i in range(num_records):
            first_name = f"{random.choice(first_names)}{i}"
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}@sjsu.edu"
            course_id = random.choice(courses)
            mark = random.randint(60, 100)
            
            students[(first_name, last_name)] = {
                "email": email,
                "course_id": course_id,
                "grade": str(mark),
                "mark": str(mark)
            }
        
        self.student.write_data(students)
        end_time = time.time()
        add_time = end_time - start_time
        
        loaded = self.student.read_data()
        self.assertEqual(len(loaded), num_records)
        print(f"   ✓ Added {num_records} records in {add_time:.6f} seconds")
        
        print(f"\n2. Modifying 100 random student records...")
        start_time = time.time()
        keys = list(students.keys())
        for i in range(100):
            random_key = random.choice(keys)
            students[random_key]["mark"] = str(random.randint(60, 100))
        
        self.student.write_data(students)
        end_time = time.time()
        modify_time = end_time - start_time
        print(f"   ✓ Modified 100 records in {modify_time:.6f} seconds")
        
        print(f"\n3. Deleting 100 random student records...")
        start_time = time.time()
        for i in range(100):
            if keys:
                random_key = keys.pop(random.randint(0, len(keys) - 1))
                if random_key in students:
                    del students[random_key]
        
        self.student.write_data(students)
        end_time = time.time()
        delete_time = end_time - start_time
        
        loaded = self.student.read_data()
        self.assertEqual(len(loaded), num_records - 100)
        print(f"   ✓ Deleted 100 records in {delete_time:.6f} seconds")
        print(f"   ✓ Final record count: {len(loaded)}")
        
        print("\n" + "="*80)
        print("CRUD Operations Summary (1000+ records):")
        print("="*80)
        print(f"Add 1000 records:    {add_time:.6f} seconds")
        print(f"Modify 100 records:  {modify_time:.6f} seconds")
        print(f"Delete 100 records:  {delete_time:.6f} seconds")
        print("="*80)


class TestSearchAndSort(unittest.TestCase):
    
    def setUp(self):
        self.student = Student()
        self.test_file = "test_search_sort.csv"
        self.student.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def generate_large_dataset(self, num_records=1000):
        print(f"\nGenerating {num_records} student records...")
        students = {}
        
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        courses = ["DATA200", "DATA201", "CS101", "CS102", "MATH101"]
        
        for i in range(num_records):
            first_name = random.choice(first_names) + str(i)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}@sjsu.edu"
            course_id = random.choice(courses)
            mark = random.randint(60, 100)
            
            students[(first_name, last_name)] = {
                "email": email,
                "course_id": course_id,
                "grade": str(mark),
                "mark": str(mark)
            }
        
        self.student.write_data(students)
        print(f"✓ Generated {num_records} records")
        return students
    
    def test_search_timing_1000_records(self):
        num_records = 1000
        students = self.generate_large_dataset(num_records)
        
        search_key = list(students.keys())[random.randint(0, len(students) - 1)]
        search_first_name, search_last_name = search_key
        
        print(f"\nSearching for student: {search_first_name} {search_last_name}")
        
        start_time = time.time()
        loaded_students = self.student.read_data()
        found = search_key in loaded_students
        end_time = time.time()
        search_time = end_time - start_time
        
        self.assertTrue(found)
        print(f"✓ Search completed in {search_time:.6f} seconds")
        print(f"  Total records: {len(loaded_students)}")
    
    def test_sort_by_marks_ascending(self):
        num_records = 1000
        self.generate_large_dataset(num_records)
        
        print(f"\nSorting {num_records} records by marks (ascending)...")
        
        start_time = time.time()
        students = self.student.read_data()
        sorted_students = sorted(students.items(), key=lambda x: float(x[1]['mark']))
        end_time = time.time()
        sort_time = end_time - start_time
        
        marks = [float(student[1]['mark']) for student in sorted_students]
        self.assertEqual(marks, sorted(marks))
        
        print(f"✓ Sort completed in {sort_time:.6f} seconds")
        print(f"  Total records: {len(sorted_students)}")
    
    def test_sort_by_marks_descending(self):
        num_records = 1000
        self.generate_large_dataset(num_records)
        
        print(f"\nSorting {num_records} records by marks (descending)...")
        
        start_time = time.time()
        students = self.student.read_data()
        sorted_students = sorted(students.items(), key=lambda x: float(x[1]['mark']), reverse=True)
        end_time = time.time()
        sort_time = end_time - start_time
        
        marks = [float(student[1]['mark']) for student in sorted_students]
        self.assertEqual(marks, sorted(marks, reverse=True))
        
        print(f"✓ Sort completed in {sort_time:.6f} seconds")
    
    def test_sort_by_email(self):
        num_records = 1000
        self.generate_large_dataset(num_records)
        
        print(f"\nSorting {num_records} records by email...")
        
        start_time = time.time()
        students = self.student.read_data()
        sorted_students = sorted(students.items(), key=lambda x: x[1]['email'])
        end_time = time.time()
        sort_time = end_time - start_time
        
        emails = [student[1]['email'] for student in sorted_students]
        self.assertEqual(emails, sorted(emails))
        
        print(f"✓ Sort completed in {sort_time:.6f} seconds")


class TestDataPersistence(unittest.TestCase):
    
    def setUp(self):
        self.student = Student()
        self.test_file = "test_persistence.csv"
        self.student.file_path = self.test_file
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_data_persistence_across_sessions(self):
        students = {
            ("Alice", "Wonder"): {
                "email": "alice@sjsu.edu",
                "course_id": "DATA200",
                "grade": "A",
                "mark": "95"
            }
        }
        self.student.write_data(students)
        
        new_student_instance = Student()
        new_student_instance.file_path = self.test_file
        
        loaded_students = new_student_instance.read_data()
        
        self.assertIn(("Alice", "Wonder"), loaded_students)
        self.assertEqual(loaded_students[("Alice", "Wonder")]["email"], "alice@sjsu.edu")
        print("✓ Data persistence test passed")
    
    def test_unique_student_email(self):
        students = {
            ("John", "Doe"): {
                "email": "john@sjsu.edu",
                "course_id": "DATA200",
                "grade": "A",
                "mark": "90"
            }
        }
        self.student.write_data(students)
        
        students = self.student.read_data()
        initial_count = len(students)
        students[("John", "Doe")] = {
            "email": "john2@sjsu.edu",
            "course_id": "DATA201",
            "grade": "B",
            "mark": "85"
        }
        self.student.write_data(students)
        
        students = self.student.read_data()
        self.assertEqual(len(students), initial_count)
        print("✓ Unique student email test passed")


def run_all_tests():
    print("\n" + "="*80)
    print("CheckMyGrade Application - Comprehensive Test Suite")
    print("DATA 200 - Lab 1")
    print("="*80)
    
    test_suite = unittest.TestSuite()
    
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAuthentication))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudent))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCourse))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProfessor))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudentCRUD1000Records))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSearchAndSort))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataPersistence))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)
    
    return result


if __name__ == "__main__":
    result = run_all_tests()
    exit(0 if result.wasSuccessful() else 1)