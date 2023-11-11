# Jesters Password Manager

This is a simple command-line password manager implemented in Python. It allows you to securely store and manage your passwords for various websites and accounts. The passwords are encrypted using Blowfish encryption and can only be decrypted with your secret key.

## Features

- Add new passwords
- View passwords for specific accounts
- View all stored passwords
- Import passwords from a CSV file
- Export passwords to a CSV file
- Generate strong passwords
- Securely store your secret key

## Getting Started

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/J3ST3RPY/Jesters_Password_Manager.git
   ```

2. Install the required dependencies:

   ```
   pip3 install pycryptodome colorama
   ```

3. Run the password manager:

   ```
   python3 main.py
   ```
## Usage
Here are the main options available in the menu:

1. Add a password: You can add a new password for a specific website and account.

2. View a password: You can view the password for a specific account.

3. View all passwords: View all stored passwords.

4. Import passwords from CSV: You can import passwords from a CSV file to quickly populate your password manager.

5. Export passwords to CSV: Export all stored passwords to a CSV file for backup or sharing.

6. Generate a strong password: Generate a random strong password using a mix of uppercase letters, lowercase letters, digits, and special characters.

## Security Note

**Please ensure the safety of your secret key.**

Your secret key is vital for decrypting your stored passwords. If you lose or forget your secret key, there is no way to recover your passwords. Keep it in a secure and memorable location to maintain access to your stored information.

## Contributing

**We welcome contributions!**

If you have ideas for improving this password manager or wish to introduce new features, we encourage you to fork this repository and submit a pull request. Your contributions help make this tool more robust and feature-rich.

## License

**Licensed under the MIT License**

This project is open-source and distributed under the MIT License.

## Acknowledgments

This password manager relies on the PyCryptodome library for encryption and the Colorama library for enhancing console output with colors. We appreciate the contributions of these projects to make our password manager more secure and user-friendly.

Thank you for choosing and using the Khetsus Password Manager! Your support and feedback are greatly appreciated.
