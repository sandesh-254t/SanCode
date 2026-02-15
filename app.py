from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

# ===============================
# LANDING PAGE
# ===============================
@app.route("/")
def landing():
    return render_template("landing.html")


# ===============================
# IDE PAGE
# ===============================
@app.route("/ide")
def ide():
    return render_template("index.html")


# ===============================
# DOCS PAGE
# ===============================
@app.route("/docs")
def docs():
    return render_template("docs.html")


# ===============================
# ABOUT PAGE
# ===============================
@app.route("/about")
def about():
    return render_template("about.html")


# ===============================
# LEARN MAIN PAGE
# ===============================
@app.route("/learn")
def learn():
    return render_template("learn.html")


# ===============================
# LEARN SUB PAGES
# ===============================

@app.route("/learn/printing")
def learn_printing():
    return render_template("learn_printing.html")


@app.route("/learn/variables")
def learn_variables():
    return render_template("learn_variables.html")


@app.route("/learn/conditions")
def learn_conditions():
    return render_template("learn_conditions.html")


@app.route("/learn/otherwise")
def learn_otherwise():
    return render_template("learn_otherwise.html")


# ===============================
# RUN SANCODE
# ===============================
@app.route("/run", methods=["POST"])
def run_code():
    try:
        code = request.json["code"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".g", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(code)
            temp_filename = temp_file.name

        result = subprocess.run(
            ["python", "lan.py", temp_filename],
            capture_output=True,
            text=True
        )

        os.remove(temp_filename)

        output = result.stdout if result.stdout else result.stderr

        return jsonify({"output": output})

    except Exception as e:
        return jsonify({"output": str(e)})


# ===============================
# START SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
