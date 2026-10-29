
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("registration.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return "All fields are required", 400

    return render_template("success.html", name=name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
