from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Calculator</title>
  <style>
    :root {
      --bg: #0f1221;
      --panel: #171a2b;
      --panel-2: #1e2238;
      --key: #2a2f4a;
      --key-hover: #343a5a;
      --op: #ff7a18;
      --op-hover: #ff8f3a;
      --muted: #9aa3b2;
      --text: #f6f7fb;
      --danger: #ff4d4d;
      --radius: 18px;
    }
    * { box-sizing: border-box; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }
    body {
      margin: 0; min-height: 100vh; display: grid; place-items: center;
      background: radial-gradient(1200px 800px at 20% -10%, #1c2140, transparent),
                  radial-gradient(900px 700px at 110% 10%, #2b1653, transparent),
                  var(--bg);
      color: var(--text);
      padding: 24px;
    }
    .wrap {
      width: min(380px, 96vw);
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border-radius: 24px;
      box-shadow: 0 20px 60px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.04);
      padding: 18px;
      border: 1px solid rgba(255,255,255,.06);
    }
    .brand {
      display:flex; align-items:center; justify-content:space-between;
      margin: 4px 6px 10px;
    }
    .brand h1 {
      font-size: 14px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
      margin:0;
    }
    .screen {
      background: #0a0d1a;
      border-radius: var(--radius);
      padding: 14px 14px 10px;
      min-height: 96px;
      display:flex; flex-direction:column; justify-content:center; gap:6px;
      border: 1px solid rgba(255,255,255,.06);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.02);
      margin-bottom: 12px;
    }
    .history {
      font-size: 13px; color: var(--muted); min-height: 18px; text-align: right;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .display {
      font-size: 34px; font-weight: 600; text-align: right;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .keys {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }
    button {
      height: 56px; border: 0; border-radius: 14px;
      background: var(--key); color: var(--text); font-size: 20px; font-weight: 600;
      cursor: pointer; transition: .12s ease;
      box-shadow: 0 6px 14px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.06);
    }
    button:hover { background: var(--key-hover); transform: translateY(-1px); }
    button:active { transform: translateY(1px) scale(.98); }
    .op { background: var(--op); color: #111; }
    .op:hover { background: var(--op-hover); }
    .wide { grid-column: span 2; }
    .danger { background: #3a1c1c; color: #ffdada; }
    .danger:hover { background: #4a2222; }
    .eq { background: #4ad66d; color: #07130a; }
    .eq:hover { background: #65e381; }
    .footer {
      margin-top: 10px; font-size: 12px; color: var(--muted); text-align:center;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="brand">
      <h1>Simple Calculator</h1>
      <div style="font-size:12px;color:var(--muted)">Flask UI</div>
    </div>

    <div class="screen">
      <div id="history" class="history"></div>
      <div id="display" class="display">0</div>
    </div>

    <div class="keys">
      <button class="danger" data-action="clear">C</button>
      <button data-action="back">⌫</button>
      <button data-action="pow">^</button>
      <button class="op" data-op="div">÷</button>

      <button data-num="7">7</button>
      <button data-num="8">8</button>
      <button data-num="9">9</button>
      <button class="op" data-op="mul">×</button>

      <button data-num="4">4</button>
      <button data-num="5">5</button>
      <button data-num="6">6</button>
      <button class="op" data-op="sub">−</button>

      <button data-num="1">1</button>
      <button data-num="2">2</button>
      <button data-num="3">3</button>
      <button class="op" data-op="add">+</button>

      <button class="wide" data-num="0">0</button>
      <button data-num=".">.</button>
      <button class="eq" data-action="equals">=</button>
    </div>

    <div class="footer">Tip: you can also call the API directly at <code>/calc</code></div>
  </div>

<script>
  const display = document.getElementById("display");
  const history = document.getElementById("history");

  let current = "0";
  let first = null;
  let op = null;
  let justEvaluated = false;

  function setDisplay(val) {
    display.textContent = val;
  }

  function appendNum(n) {
    if (justEvaluated) {
      current = "0";
      justEvaluated = false;
    }
    if (current === "0" && n !== ".") current = "";
    if (n === "." && current.includes(".")) return;
    current += n;
    setDisplay(current);
  }

  function backspace() {
    if (justEvaluated) return;
    current = current.length > 1 ? current.slice(0, -1) : "0";
    setDisplay(current);
  }

  function clearAll() {
    current = "0";
    first = null;
    op = null;
    justEvaluated = false;
    history.textContent = "";
    setDisplay(current);
  }

  function setOp(newOp) {
    if (op && first !== null && !justEvaluated) {
      // chain operations
      equals();
    }
    first = parseFloat(current);
    op = newOp;
    history.textContent = `${first} ${symbolFor(op)}`;
    justEvaluated = true;
  }

  function symbolFor(o) {
    return { add:"+", sub:"−", mul:"×", div:"÷", pow:"^" }[o] || "";
  }

  async function equals() {
    if (op === null || first === null) return;
    const second = parseFloat(current);

    // call backend API
    const url = `/calc?op=${op}&a=${first}&b=${second}`;
    const res = await fetch(url);
    const data = await res.json();

    if (!res.ok) {
      history.textContent = data.error || "Error";
      setDisplay("0");
      current = "0";
      op = null;
      first = null;
      return;
    }

    history.textContent = `${first} ${symbolFor(op)} ${second} =`;
    current = String(data.result);
    setDisplay(current);
    first = null;
    op = null;
    justEvaluated = true;
  }

  function power() {
    setOp("pow");
  }

  document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
      const num = btn.getAttribute("data-num");
      const o = btn.getAttribute("data-op");
      const action = btn.getAttribute("data-action");

      if (num !== null) return appendNum(num);
      if (o) return setOp(o);

      if (action === "back") return backspace();
      if (action === "clear") return clearAll();
      if (action === "equals") return equals();
      if (action === "pow") return power();
    });
  });
</script>
</body>
</html>
"""


@app.get("/calc")
def calc():
    op = request.args.get("op", "").lower()
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify(error="Please provide numbers a and b"), 400

    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        if b == 0:
            return jsonify(error="Division by zero not allowed"), 400
        result = a / b
    elif op == "pow":
        result = a ** b
    else:
        return jsonify(error="Invalid op. Use add, sub, mul, div, pow"), 400

    return jsonify(op=op, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
