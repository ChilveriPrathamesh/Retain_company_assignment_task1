# CHANGES.md

## 🔍 Major Issues Identified in Legacy Code

- ❌ All logic was in a single file (`app.py`), violating separation of concerns.
- ❌ SQL queries were vulnerable to SQL injection (e.g., string interpolation).
- ❌ Passwords were stored and compared in plain text.
- ❌ No input validation or error handling.
- ❌ Inconsistent HTTP status codes and raw string responses.
- ❌ Global, persistent database connection (risk of locking and resource leaks).

---

## ✅ Changes Made

### ✅ Security Improvements
- Replaced all raw SQL queries with **parameterized** ones using `?` placeholders.
- Implemented **bcrypt** to securely hash passwords.
- Added **password comparison** with hash checking during login.

### ✅ Code Structure
- Split logic into modular files:
  - `routes/users.py`: All user routes
  - `schemas/user_schema.py`: Input validation using Marshmallow
  - `utils/security.py`: Password hashing utilities
  - `db.py`: Handles DB connection safely

### ✅ Validation & Error Handling
- Used Marshmallow to validate request inputs.
- Returned JSON responses with proper **HTTP status codes**.
- Added guards for missing fields and invalid data.

### ✅ Maintainability
- Simplified `app.py` to just route registration.
- Removed redundant logging/printing from endpoints.

---

## 📚 Tools / AI Used

- **ChatGPT**:
  - For guidance on refactoring Flask applications.
  - Helped design modular structure and `bcrypt` integration.
  - Generated Marshmallow schema examples and validation logic.
  - Assisted in identifying SQL injection issues and standard fixes.

- **Manual Work**:
  - All code reviewed, modified, and tested locally.
  - AI-suggested code was edited and integrated after understanding its logic.

---

## 🧠 Assumptions / Trade-offs

- Email uniqueness was assumed and enforced in DB.
- Did not use JWT-based session management due to time limits.
- Did not add pagination or filtering on `/users`.

---

## 🚀 What I Would Do With More Time

- Add **JWT authentication** with protected routes.
- Implement **rate limiting** and request logging.
- Add **unit tests** and **integration tests** using `pytest`.
- Deploy the API using Docker and expose via Swagger/OpenAPI.

---

## 🔧 How to Run the App

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the server
python app.py
