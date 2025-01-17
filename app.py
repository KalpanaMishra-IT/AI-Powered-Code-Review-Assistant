from flask import Flask, render_template, request
from analyzer import analyze_code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        code_snippet = request.form["code"]
        print("code_snippet-->\n",code_snippet)
        result = analyze_code(code_snippet)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=False)
