from flask import Flask
from flask import render_template, redirect, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run(debug=True)
