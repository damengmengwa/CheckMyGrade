import os
import hashlib
import click

class Authentication:
    def __init__(self):
        self.file_path = "authentication.csv"

    def read_data(self):
        accounts = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        role, email, encrypted_password = line.split(",")
                        accounts[email] = {"role": role, "password": encrypted_password}
                    except ValueError as e:
                        click.echo(f"Warning: Skipping malformed line in {self.file_path}: {line}")
                        continue
        return accounts

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            for email, info in data.items():
                file.write(f"{info['role']},{email},{info['password']}\n")

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_not_null(self, value, field_name):
        if not value or value.strip() == "":
            click.echo(f"Error: {field_name} cannot be empty.")
            return False
        return True

    def create_new_account(self, email, password, role):
        accounts = self.read_data()

        if not self.validate_not_null(email, "Email"):
            return

        if not self.validate_not_null(password, "Password"):
            return

        if email in accounts:
            click.echo("Account already exists.")
            return

        encrypted_password = self.encrypt_password(password)
        accounts[email] = {
            "role": role,
            "password": encrypted_password
        }
        self.write_data(accounts)
        click.echo("Account created successfully")

    def login(self, email, password):
        accounts = self.read_data()

        if email not in accounts:
            click.echo("Account does not exist.")
            return None

        encrypted_password = self.encrypt_password(password)
        if accounts[email]["password"] == encrypted_password:
            return accounts[email]["role"]
        else:
            click.echo("Incorrect password")
            return None

    def change_password(self, email, old_password, new_password):
        accounts = self.read_data()

        if email not in accounts:
            click.echo("Account does not exist")
            return

        encrypted_old_password = self.encrypt_password(old_password)
        if accounts[email]["password"] != encrypted_old_password:
            click.echo("Old password is incorrect")
            return
        
        accounts[email]["password"] = self.encrypt_password(new_password)
        self.write_data(accounts)
        click.echo("Password changed successfully")

    def print_account_details(self, email):
        accounts = self.read_data()

        if email not in accounts:
            click.echo("Account not found.")
            return

        info = accounts[email]
        click.echo(f"Email: {email}, Role: {info['role']}, Encrypted Password: {info['password']}")