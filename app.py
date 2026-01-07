from flask import Flask, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape

app = Flask(__name__)

def start_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
#To prevent clashes in databases
    cursor.execute("DELETE FROM users")

    hashed_password = generate_password_hash("123")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", hashed_password)
    )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Hello, this is my app"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
#checks if given and stored password is same
        if user and check_password_hash(user[2], password):
            return "Login successful"
        else:
            return "Login failed"

    return '''
        <form method="POST">
            <input name="username" placeholder="username">
            <input name="password" placeholder="password">
            <button type="submit">Login</button>
        </form>
    '''
#Helps in preventing XSS by making browser read the HTML text
@app.route("/echoed")
def echo():
    msg = request.args.get("msg", "")
    return f"You said: {escape(msg)}"



start_db()

if __name__ == "__main__":
    app.run(debug=True)
