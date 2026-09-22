try:
    import bcrypt
except ImportError as e:
    raise ImportError(
        "Missing dependency 'bcrypt'. Install it with: pip install bcrypt"
    ) from e
from database import get_connection


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT UserID FROM Users WHERE Username = ?",
        (username,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def validate_registration(
    full_name,
    username,
    password,
    confirm_password,
    email
):
    if not full_name.strip():
        return "Full name cannot be blank."

    if not username.strip():
        return "Username cannot be blank."

    if len(username) < 3:
        return "Username must be at least 3 characters."

    if not password:
        return "Password cannot be blank."

    if len(password) < 6:
        return "Password must be at least 6 characters."

    if password != confirm_password:
        return "Passwords do not match."

    if not email.strip():
        return "Email cannot be blank."

    if "@" not in email or "." not in email:
        return "Invalid email format."

    if username_exists(username):
        return "Username already exists."

    return None


def register_user(full_name, username, password, email):
    try:
        # Validate required information
        validation_error = validate_registration(
            full_name,
            username,
            password,
            password,
            email
        )

        if validation_error:
            return False, validation_error

        # Hash password before storing it
        password_hash = hash_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Users
            (FullName, Username, PasswordHash, Email)
            VALUES (?, ?, ?, ?)
            """,
            (
                full_name,
                username,
                password_hash,
                email
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return True, "Registration successful! Your account has been created."

    except Exception as e:
        return False, f"Registration failed: {e}"


def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                UserID,
                FullName,
                Username,
                PasswordHash,
                Email,
                DateRegistered
            FROM Users
            WHERE Username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Generic error message for invalid login
        if user is None:
            return False, "Invalid username or password.", None

        # Verify password against bcrypt hash
        if not verify_password(password, user.PasswordHash):
            return False, "Invalid username or password.", None

        user_data = {
            "user_id": user.UserID,
            "full_name": user.FullName,
            "username": user.Username,
            "email": user.Email,
            "date_registered": user.DateRegistered
        }

        return True, "Login successful!", user_data

    except Exception as e:
        return False, f"Login failed: {e}", None