# --- main.py ---

import sys
import getpass

from auth import register_user, login_user


def print_header(title: str):
    """Prints a styled CLI banner header."""
    print("\n" + "=" * 45)
    print(f" {title.center(43)} ")
    print("=" * 45)


def registration_screen():
    """Handles the user registration interaction."""
    print_header("REGISTER NEW USER")
    print("Please fill in the required account details.\n")

    full_name = input("Full Name        : ").strip()
    username = input("Username         : ").strip()

    # Use getpass for masked input; fallback to input() if not supported
    try:
        password = getpass.getpass("Password         : ")
        confirm_password = getpass.getpass("Confirm Password : ")
    except Exception:
        password = input("Password         : ")
        confirm_password = input("Confirm Password : ")

    email = input("Email Address    : ").strip()

    # Client-side confirmation check
    if password != confirm_password:
        print("\n[-] Registration Failed: Passwords do not match!")
        input("\nPress Enter to return to main menu...")
        return

    success, message = register_user(
        full_name,
        username,
        password,
        email
    )

    if success:
        print(f"\n[+] {message}")
    else:
        print(f"\n[-] {message}")

    input("\nPress Enter to continue...")


def login_screen():
    """
    Handles the login sequence.
    Enforces a strict maximum of 3 failed attempts.
    """
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        print_header("USER LOGIN")

        attempts_left = max_attempts - attempts
        print(f"Attempts remaining: {attempts_left}\n")

        username = input("Username: ").strip()

        try:
            password = getpass.getpass("Password: ")
        except Exception:
            password = input("Password: ")

        success, message, user_data = login_user(
            username,
            password
        )

        if success:
            print(f"\n[+] {message}")
            input("Press Enter to proceed to your dashboard...")
            dashboard_screen(user_data)
            return

        else:
            attempts += 1

            print(f"\n[-] {message}")

            if attempts < max_attempts:
                retry = input("Try again? (y/n): ").strip().lower()

                if retry != "y":
                    return

            else:
                print("\n[!] Maximum login attempts exceeded.")
                print("For security reasons, returning to main menu.\n")
                input("Press Enter to continue...")
                return


def profile_screen(user_data: dict):
    """Displays the authenticated user profile information."""
    print_header("MY PROFILE")

    print(f"  User ID         : {user_data.get('user_id')}")
    print(f"  Full Name       : {user_data.get('full_name')}")
    print(f"  Username        : {user_data.get('username')}")
    print(f"  Email           : {user_data.get('email')}")
    print(f"  Date Registered : {user_data.get('date_registered')}")

    print("-" * 45)
    print("  [Security Note: Password & Hash are strictly hidden]")
    print("=" * 45)

    input("\nPress Enter to return to Dashboard...")


def dashboard_screen(user_data: dict):
    """
    Displays the personalized user dashboard.
    The greeting dynamically pulls the user's FullName from the database.
    """

    while True:
        print_header("USER DASHBOARD")

        # Dynamically display the FullName retrieved from Microsoft Access
        print(f"Welcome, {user_data.get('full_name')}!\n")

        print("You have successfully logged in to the database system.\n")

        print("  1. View Profile")
        print("  2. Logout")
        print("-" * 45)

        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            profile_screen(user_data)

        elif choice == "2":
            print("\n[+] You have successfully logged out.")
            input("Press Enter to return to the Main Menu...")
            break

        else:
            print("\n[-] Invalid option! Please select 1 or 2.")
            input("Press Enter to continue...")


def main_menu():
    """Entry point and primary application loop."""

    while True:
        print_header("USER AUTHENTICATION SYSTEM")

        print("  1. Register New Account")
        print("  2. Login to System")
        print("  3. Exit Application")
        print("-" * 45)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            registration_screen()

        elif choice == "2":
            login_screen()

        elif choice == "3":
            print_header("SYSTEM SHUTDOWN")
            print("Thank you for using the DBMS Authentication System.")
            print("Goodbye!\n")
            sys.exit(0)

        else:
            print("\n[-] Invalid choice! Please enter 1, 2, or 3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
    