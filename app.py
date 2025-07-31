from flask import Flask, render_template, request
import string

app = Flask(__name__)

def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 12 and score == 4:
        return "Strong ✅", "Great job!"
    elif length >= 8 and score >= 3:
        return "Moderate ⚠️", "Try adding more symbols or length."
    else:
        return "Weak ❌", "Use at least 8 characters, and mix letters, numbers, and symbols."

@app.route("/", methods=["GET", "POST"])
def index():
    strength, tip = "", ""
    if request.method == "POST":
        password = request.form["password"]
        strength, tip = check_password_strength(password)
    return render_template("index.html", strength=strength, tip=tip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
