from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Bisection Calculator</title>
    <style>
        body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f3f4f6; color: #1f2937; margin: 0; padding: 40px 15px; }
        .container { max-width: 700px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 24px; margin: 0 0 8px 0; }
        .header p { font-size: 14px; color: #4b5563; margin: 0; }
        .card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); }
        .card h3 { margin-top: 0; margin-bottom: 20px; font-size: 16px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-size: 13px; font-weight: bold; margin-bottom: 5px; color: #4b5563; }
        input[type="text"], input[type="number"], select { width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; box-sizing: border-box; font-size: 14px; background-color: #ffffff; color: #1f2937; }
        .inline-inputs { display: table; width: 100%; }
        .inline-col { display: table-cell; width: 50%; }
        .inline-col:first-child { padding-right: 10px; }
        .inline-col:last-child { padding-left: 10px; }
        button.compute-btn { width: 100%; padding: 12px; background-color: #2563eb; color: #ffffff; border: none; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 5px; }
        button.compute-btn:hover { background-color: #1d4ed8; }
        .root-display { display: inline-block; background-color: #eff6ff; color: #2563eb; font-weight: bold; font-size: 16px; padding: 8px 16px; border-radius: 6px; margin: 20px 0 10px 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: center; font-size: 13px; border-bottom: 1px solid #e5e7eb; }
        th { background-color: #f9fafb; color: #4b5563; font-weight: bold; }
        .text-red { color: #ef4444; font-weight: bold; }
        .text-green { color: #10b981; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>PIT Project – Numerical Methods Online Calculator</h1>
            <p>Using Flask (Python)</p>
        </div>
        <div class="card">
            <h3>Calculator Configuration</h3>
            <div class="form-group">
                <label for="presets">Active Preset</label>
                <select id="presets" onchange="loadPreset()">
                    <option value="eq1">f(x) = x^3 - x - 2</option>
                    <option value="eq2">f(x) = x^2 - 4</option>
                    <option value="eq3">f(x) = sin(x)</option>
                </select>
            </div>
            <div class="form-group">
                <label for="equation">Target Function f(x)</label>
                <input type="text" id="equation" value="x^3 - x - 2">
            </div>
            <div class="inline-inputs">
                <div class="inline-col">
                    <div class="form-group">
                        <label for="inputA">Lower Bound (a)</label>
                        <input type="number" id="inputA" value="1" step="any">
                    </div>
                </div>
                <div class="inline-col">
                    <div class="form-group">
                        <label for="inputB">Upper Bound (b)</label>
                        <input type="number" id="inputB" value="2" step="any">
                    </div>
                </div>
            </div>
            <button class="compute-btn" onclick="computeBisection()">Compute Roots</button>
            <div id="calculator-output"></div>
        </div>
    </div>
    <script>
        function loadPreset() {
            var p = document.getElementById('presets').value;
            var eqInput = document.getElementById('equation');
            var aInput = document.getElementById('inputA');
            var bInput = document.getElementById('inputB');
            if (p === 'eq1') { eqInput.value = "x^3 - x - 2"; aInput.value = "1"; bInput.value = "2"; }
            if (p === 'eq2') { eqInput.value = "x^2 - 4"; aInput.value = "0"; bInput.value = "3"; }
            if (p === 'eq3') { eqInput.value = "sin(x)"; aInput.value = "3"; bInput.value = "4"; }
        }
        function evalFunc(expr, x) {
            try {
                var safe = expr.replace(/\^/g, '**').replace(/(\d)(x)/g, '$1*$2')
                               .replace(/sin/g, 'Math.sin').replace(/cos/g, 'Math.cos').replace(/pi/g, 'Math.PI');
                return new Function('x', 'return ' + safe)(x);
            } catch(e) { return NaN; }
        }
        function computeBisection() {
            var expr = document.getElementById('equation').value;
            var a = parseFloat(document.getElementById('inputA').value);
            var b = parseFloat(document.getElementById('inputB').value);
            var out = document.getElementById('calculator-output');
            out.innerHTML = "";
            if (isNaN(a) || isNaN(b) || !expr.trim()) { out.innerHTML = "<p style='color:red; font-weight:bold; margin-top:15px;'>❌ Please enter valid inputs.</p>"; return; }
            var fa = evalFunc(expr, a); var fb = evalFunc(expr, b);
            if (isNaN(fa) || isNaN(fb)) { out.innerHTML = "<p style='color:red; font-weight:bold; margin-top:15px;'>❌ Invalid equation syntax.</p>"; return; }
            if (fa * fb >= 0) { out.innerHTML = "<p style='color:red; font-weight:bold; margin-top:15px;'>❌ f(a) and f(b) must have opposite signs.</p>"; return; }
            var tableHTML = "<h3>Iteration History Logs</h3><table><thead><tr><th>Iter</th><th>a</th><th>b</th><th>c</th><th>f(c)</th></tr></thead><tbody>";
            var c = a;
            for (var i = 1; i <= 14; i++) {
                c = (a + b) / 2; var fc = evalFunc(expr, c); var fcClass = fc < 0 ? 'text-red' : 'text-green';
                tableHTML += "<tr><td><strong>" + i + "</strong></td><td>" + a.toFixed(6) + "</td><td>" + b.toFixed(6) + "</td><td>" + c.toFixed(6) + "</td><td class='" + fcClass + "'>" + fc.toFixed(6) + "</td></tr>";
                if (evalFunc(expr, a) * fc < 0) { b = c; } else { a = c; }
            }
            tableHTML += "</tbody></table>";
            out.innerHTML = "<div class='root-display'>Approx Root: " + c + "</div>" + tableHTML;
        }
    </script>
</body>
</html>
"""

# The explicit root rule that satisfies Vercel's app layout engine
@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == "__main__":
    app.run(debug=True)
