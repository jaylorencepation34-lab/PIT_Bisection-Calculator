from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Function example (you can let user change later if needed)
def f(x):
    return x**3 - x - 2


def bisection(a, b, tol=0.0001, max_iter=50):
    if f(a) * f(b) >= 0:
        return None, "Invalid interval: f(a) and f(b) must have opposite signs."

    steps = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        steps.append((i+1, a, b, c, fc))

        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, steps

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return c, steps


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    steps = None
    error = None

    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])

        result, steps = bisection(a, b)

        if steps == "Invalid interval: f(a) and f(b) must have opposite signs.":
            error = steps
            steps = None

    return render_template("bisection.html", result=result, steps=steps, error=error)


if __name__ == "__main__":
    app.run(debug=True)