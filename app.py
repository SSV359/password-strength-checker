from flask import Flask, render_template, request
import string
import secrets
import random

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
    # Completely random strong password (for blank input)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            break
    recommendation = (
        "This password is highly secure due to its length and use of random characters, numbers, and symbols. "
        "Consider using a password manager to store it safely."
    )
    return password, recommendation

def ai_suggest_similar_password(user_password):
    # If input is too short, just use random suggestion
    if len(user_password) < 4:
        return ai_suggest_password()
    # Capitalize first letter if not already
    base = user_password
    if base and not base[0].isupper():
        base = base.capitalize()
    # Pad to at least 8 chars if needed
    while len(base) < 8:
        base += str(random.randint(0, 9))
    # Add a strong random suffix
    suffix = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
    strong_password = base + suffix
    # Ensure all character types and length >= 12
    while (not any(c.isupper() for c in strong_password) or
           not any(c.islower() for c in strong_password) or
           not any(c.isdigit() for c in strong_password) or
           not any(c in string.punctuation for c in strong_password) or
           len(strong_password) < 12):
        strong_password += secrets.choice(string.ascii_letters + string.digits + string.punctuation)
    recommendation = (
        "This AI-suggested password keeps your original idea, but adds length, symbols, and random characters for higher security. "
        "It's much stronger but still feels familiar. Consider using a password manager to save it."
    )
    return strong_password, recommendation

@app.route("/", methods=["GET", "POST"])
def index():
    strength, tip, suggestion, suggestion_tip = "", "", "", ""
    password = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        if "suggest" in request.form:
            if password:
                suggestion, suggestion_tip = ai_suggest_similar_password(password)
            else:
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
