from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import hashlib
import json
import csv
import random
import string
import os
from time import sleep
from colorama import Fore,Style

def generate_password(length=16):
	uppercase_letters = string.ascii_uppercase
	lowercase_letters = string.ascii_lowercase
	digits = string.digits
	special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
	all_characters = uppercase_letters + lowercase_letters + digits + special_characters
	password = (
		random.choice(uppercase_letters)
		+ random.choice(lowercase_letters)
		+ random.choice(digits)
		+ random.choice(special_characters)
	)
	for _ in range(length - 4):
		password += random.choice(all_characters)
	password_list = list(password)
	random.shuffle(password_list)
	password = "".join(password_list)
	return password


def clear():
	if os.name == "nt":
		_ = os.system("cls")
	else:
		_ = os.system("clear")


def load_secret_key():
	if os.path.exists("secret_key.bin"):
		with open("secret_key.bin", "rb") as key_file:
			hashed_key = key_file.read()
		return hashed_key
	else:
		return None


def save_secret_key(secret_key):
	hashed_key = hashlib.sha256(secret_key.encode()).digest()
	with open("secret_key.bin", "wb") as key_file:
		key_file.write(hashed_key)
	print("Secret key set securely.")


def encrypt_message(message, key):
	cipher = Blowfish.new(key, Blowfish.MODE_ECB)
	message = pad(message.encode(), Blowfish.block_size)
	return cipher.encrypt(message).hex()


def decrypt_message(encrypted_message, key):
	cipher = Blowfish.new(key, Blowfish.MODE_ECB)
	decrypted = cipher.decrypt(bytes.fromhex(encrypted_message))
	return unpad(decrypted, Blowfish.block_size).decode()


def load_passwords():
	try:
		with open("passwords.json", "r") as file:
			return json.load(file)
	except (FileNotFoundError, json.JSONDecodeError):
		return {}


def save_passwords(passwords):
	with open("passwords.json", "w") as file:
		json.dump(passwords, file)


def import_passwords_from_csv(csv_filename, key):
	try:
		print(f"Attempting to open and read from {csv_filename}...")
		with open(csv_filename, "r", encoding="utf-8") as csv_file:
			reader = csv.reader(csv_file)
			imported_count = 0
			for row in reader:
				print(f"Read row: {row}")
				if website and account and password:
					if website not in passwords:
						passwords[website] = {}
					passwords[website][account] = encrypt_message(password, key)
					imported_count += 1
			save_passwords(passwords)
		print(f"{imported_count} passwords imported successfully.")
	except FileNotFoundError:
		print(f"File '{csv_filename}' not found.")
	except Exception as e:
		print(f"An error occurred during import: {str(e)}")


def export_passwords_to_csv(csv_filename, key):
	passwords = load_passwords()
	try:
		with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
			writer = csv.writer(csv_file)
			for website, accounts in passwords.items():
				for account, encrypted_password in accounts.items():
					decrypted_password = decrypt_message(encrypted_password, key)
					writer.writerow([website, account, decrypted_password])
		print("Passwords exported successfully.")
	except Exception as e:
		print(f"An error occurred during export: {str(e)}")


def add_password(account, password, website, key):
	passwords = load_passwords()

	if website not in passwords:
		passwords[website] = {}

	if account in passwords[website]:
		choice = (
			input(
				f"An account with the name '{account}' already exists for '{website}'.\n"
				"Do you want to (C)hange the password or (A)dd as a new account? (C/A): "
			)
			.strip()
			.lower()
		)
		if choice == "c":
			encrypted_password = encrypt_message(password, key)
			passwords[website][account] = encrypted_password
		elif choice == "a":
			account_number = 2
			while f"{account}_{account_number}" in passwords[website]:
				account_number += 1
			account = f"{account}_{account_number}"
			encrypted_password = encrypt_message(password, key)
			passwords[website][account] = encrypted_password
		else:
			print("Invalid choice. No changes were made.")
	else:
		encrypted_password = encrypt_message(password, key)
		passwords[website][account] = encrypted_password

	save_passwords(passwords)
	print("Password added successfully")


def view_password(account, key):
	passwords = load_passwords()
	encrypted_password = passwords.get(account)

	if encrypted_password:
		decrypted_password = decrypt_message(encrypted_password, key)
		print(f"Password for {account}: {decrypted_password}")
	else:
		print(f"No password found for {account}.")


def view_all_passwords(key):
	passwords = load_passwords()
	if passwords:
		print("All passwords:")
		for website, accounts in passwords.items():
			for account, encrypted_password in accounts.items():
				decrypted_password = decrypt_message(encrypted_password, key)
				print(
					f"Website: {website} \n Account: {account} \n Password: {decrypted_password}"
				)
	else:
		print("No passwords found.")


def main():
	secret_key = load_secret_key()

	if secret_key is None:
		print("Welcome! It looks like it's your first time using this program.")
		secret_key = input("Please enter your secret key: ")
		save_secret_key(secret_key)
		exit()

	user_input = input("Enter your secret key: ")
	hashed_input = hashlib.sha256(user_input.encode()).digest()

	if hashed_input == secret_key:
		print("Welcome...")
		sleep(5)
		clear()
		while True:
			print(Fore.RED + 
				"""
 ___________________
 | _______________ |                  Dont Worry ;) We wont track you.
 | |             | |       
 | |  PASSWORD   | |       1. Add a password          4. Import passwords from CSV
 | |   MANAGER   | |
 | |     BY      | |       2. View a password         5. Export passwords to CSV        
 | |   KHETSU    | |
 | |_____________| |       3. View all passwords      6. Generate a strong password
 |_________________|
	 _[_______]_
 ___[___________]___                           7. Leave
|         [_____] []|
|         [_____] []|
|___________________|"""
			)
			print("")
			choice = input("Enter your choice: ")
			if choice == "1":
				website = input("Enter the Website: ")
				account = input("Enter the account name: ")
				password = input("Enter the password: ")
				add_password(account, password, website, secret_key)
				sleep(5)
				clear()
			elif choice == "2":
				account = input("Enter the account name: ")
				view_password(account, secret_key)
			elif choice == "3":
				view_all_passwords(secret_key)
			elif choice == "4":
				csv_filename = input("Enter the CSV filename to import from: ")
				import_passwords_from_csv(csv_filename, secret_key)
				sleep(5)
				clear()
			elif choice == "5":
				csv_filename = input("Enter the CSV filename to export to: ")
				export_passwords_to_csv(csv_filename, secret_key)
				sleep(5)
				clear()
			elif choice == "6":
				clear()
				for x in range(10):
					Simulation = generate_password()
					print("Generating Password : " + Simulation)
					sleep(0.1)
					clear()
				generated_password = generate_password()
				print("Generated Password : " + generated_password)
			elif choice == "7":
				print("Exiting the password manager.")
				print(Style.RESET_ALL)
				sleep(3)
				clear()
				break
			else:
				print("Invalid choice. Please try again.")
				sleep(5)
				clear()
	else:
		print("Secret key does not match.")


if __name__ == "__main__":
	main()
