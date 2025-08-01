from flask import Flask, render_template, request
import string, secrets

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

def ai_suggest_password():
    # Generate a strong random password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        # Ensure it has at least one of each type
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            break
    recommendation = "This password is highly secure due to its length and use of random characters, numbers, and symbols. Consider using a password manager to store it safely."
    return password, recommendation

@app.route("/", methods=["GET", "POST"])
def index():
    strength, tip, suggestion, suggestion_tip = "", "", "", ""
    if request.method == "POST":
        password = request.form.get("password", "")
        if "suggest" in request.form:
            suggestion, suggestion_tip = ai_suggest_password()
        else:
            strength, tip = check_password_strength(password)
    return render_template("index.html",
        strength=strength,
        tip=tip,
        suggestion=suggestion,
        suggestion_tip=suggestion_tip
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
