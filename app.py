from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CALCULAROT</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0f;
    --panel: #0f0f1a;
    --border: #1a1a2e;
    --accent: #00ff9d;
    --accent2: #ff006e;
    --accent3: #7b2fff;
    --text: #e0e0ff;
    --dim: #4a4a6a;
    --glow: 0 0 20px rgba(0,255,157,0.4);
    --glow2: 0 0 20px rgba(255,0,110,0.4);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Share Tech Mono', monospace;
    overflow: hidden;
  }

  /* Animated grid background */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: 
      linear-gradient(rgba(0,255,157,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,255,157,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: gridMove 20s linear infinite;
    pointer-events: none;
  }

  @keyframes gridMove {
    0% { transform: translate(0,0); }
    100% { transform: translate(40px,40px); }
  }

  .wrapper {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .title {
    font-family: 'Orbitron', monospace;
    font-weight: 900;
    font-size: 2rem;
    letter-spacing: 0.3em;
    color: var(--accent);
    text-shadow: var(--glow);
    animation: pulse 3s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  .calculator {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 24px;
    width: 340px;
    box-shadow: 
      0 0 40px rgba(0,255,157,0.05),
      inset 0 0 60px rgba(0,0,0,0.5);
    position: relative;
  }

  .calculator::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent3), var(--accent2), transparent);
    animation: scanline 2s linear infinite;
  }

  @keyframes scanline {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
  }

  .display-area {
    background: #05050d;
    border: 1px solid #1a1a3a;
    border-radius: 2px;
    padding: 16px;
    margin-bottom: 20px;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 8px;
    position: relative;
    overflow: hidden;
  }

  .display-area::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,255,157,0.01) 2px,
      rgba(0,255,157,0.01) 4px
    );
    pointer-events: none;
  }

  .expression {
    color: var(--dim);
    font-size: 0.85rem;
    min-height: 20px;
    word-break: break-all;
    text-align: right;
  }

  .display {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent);
    text-shadow: var(--glow);
    word-break: break-all;
    text-align: right;
    line-height: 1;
    transition: all 0.1s;
  }

  .display.error {
    color: var(--accent2);
    text-shadow: var(--glow2);
    font-size: 1rem;
  }

  .buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
  }

  .btn {
    background: #0d0d1f;
    border: 1px solid #1a1a35;
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    font-size: 1rem;
    padding: 16px 8px;
    cursor: pointer;
    border-radius: 2px;
    transition: all 0.15s;
    position: relative;
    overflow: hidden;
  }

  .btn:hover {
    background: #131325;
    border-color: var(--accent3);
    color: var(--accent);
    box-shadow: 0 0 10px rgba(123,47,255,0.3);
    transform: translateY(-1px);
  }

  .btn:active {
    transform: translateY(1px);
    background: #1a1a35;
  }

  .btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(0,255,157,0.2), transparent 70%);
    opacity: 0;
    transition: opacity 0.2s;
  }

  .btn:active::after { opacity: 1; }

  .btn.op {
    color: var(--accent3);
    border-color: #2a1a4a;
  }
  .btn.op:hover { border-color: var(--accent3); color: #fff; }

  .btn.equals {
    background: linear-gradient(135deg, #003d26, #001a10);
    border-color: var(--accent);
    color: var(--accent);
    font-size: 1.3rem;
    box-shadow: var(--glow);
  }
  .btn.equals:hover {
    background: linear-gradient(135deg, #00602a, #003d26);
    box-shadow: 0 0 25px rgba(0,255,157,0.6);
  }

  .btn.clear {
    background: linear-gradient(135deg, #3d0020, #1a000e);
    border-color: var(--accent2);
    color: var(--accent2);
  }
  .btn.clear:hover {
    background: linear-gradient(135deg, #600030, #3d0020);
    box-shadow: var(--glow2);
  }

  .btn.span2 { grid-column: span 2; }
  .btn.span3 { grid-column: span 3; }

  .btn.func {
    color: #88aaff;
    border-color: #1a1a45;
    font-size: 0.8rem;
  }

  .status {
    text-align: center;
    color: var(--dim);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    margin-top: 12px;
  }

  .status span {
    color: var(--accent);
  }

  @keyframes resultFlash {
    0% { text-shadow: 0 0 40px rgba(0,255,157,1); }
    100% { text-shadow: var(--glow); }
  }

  .flash { animation: resultFlash 0.3s ease-out; }

  @media (max-width: 400px) {
    .calculator { width: 300px; padding: 16px; }
    .title { font-size: 1.4rem; }
  }
</style>
</head>
<body>
<div class="wrapper">
  <div class="title">CALCULAROT</div>
  <div class="calculator">
    <div class="display-area">
      <div class="expression" id="expression"></div>
      <div class="display" id="display">0</div>
    </div>
    <div class="buttons">
      <!-- Row 1 -->
      <button class="btn func" onclick="calcFunc('sin')">SIN</button>
      <button class="btn func" onclick="calcFunc('cos')">COS</button>
      <button class="btn func" onclick="calcFunc('tan')">TAN</button>
      <button class="btn func" onclick="calcFunc('sqrt')">√</button>

      <!-- Row 2 -->
      <button class="btn func" onclick="calcFunc('log')">LOG</button>
      <button class="btn func" onclick="calcFunc('ln')">LN</button>
      <button class="btn func" onclick="append('**')">xʸ</button>
      <button class="btn func" onclick="append('%')">MOD</button>

      <!-- Row 3 -->
      <button class="btn clear" onclick="clearAll()">AC</button>
      <button class="btn op" onclick="deleteLast()">DEL</button>
      <button class="btn op" onclick="toggleSign()">+/-</button>
      <button class="btn op" onclick="append('/')">÷</button>

      <!-- Row 4 -->
      <button class="btn" onclick="append('7')">7</button>
      <button class="btn" onclick="append('8')">8</button>
      <button class="btn" onclick="append('9')">9</button>
      <button class="btn op" onclick="append('*')">×</button>

      <!-- Row 5 -->
      <button class="btn" onclick="append('4')">4</button>
      <button class="btn" onclick="append('5')">5</button>
      <button class="btn" onclick="append('6')">6</button>
      <button class="btn op" onclick="append('-')">−</button>

      <!-- Row 6 -->
      <button class="btn" onclick="append('1')">1</button>
      <button class="btn" onclick="append('2')">2</button>
      <button class="btn" onclick="append('3')">3</button>
      <button class="btn op" onclick="append('+')">+</button>

      <!-- Row 7 -->
      <button class="btn" onclick="append('(')">( </button>
      <button class="btn" onclick="append('0')">0</button>
      <button class="btn" onclick="append('.')">.</button>
      <button class="btn equals" onclick="calculate()">=</button>
    </div>
    <div class="status">SYSTEM READY // PORT <span>8000</span></div>
  </div>
</div>

<script>
let current = '0';
let expression = '';
let justCalced = false;

const display = document.getElementById('display');
const exprEl = document.getElementById('expression');

function updateDisplay() {
  display.textContent = current;
  exprEl.textContent = expression;
  display.classList.remove('error');
}

function append(val) {
  if (justCalced && !isNaN(val) || justCalced && val === '.') {
    current = '';
    expression = '';
  }
  justCalced = false;

  if (current === '0' && val !== '.' && !isNaN(val)) {
    current = val;
  } else {
    current += val;
  }
  updateDisplay();
}

function clearAll() {
  current = '0';
  expression = '';
  justCalced = false;
  updateDisplay();
}

function deleteLast() {
  if (current.length <= 1) {
    current = '0';
  } else {
    current = current.slice(0, -1);
  }
  updateDisplay();
}

function toggleSign() {
  if (current !== '0') {
    current = current.startsWith('-') ? current.slice(1) : '-' + current;
    updateDisplay();
  }
}

function calcFunc(fn) {
  expression = fn + '(' + current + ')';
  fetch('/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ expression: expression })
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      display.textContent = data.error;
      display.classList.add('error');
    } else {
      current = String(data.result);
      justCalced = true;
      updateDisplay();
      display.classList.add('flash');
      setTimeout(() => display.classList.remove('flash'), 300);
    }
  });
}

function calculate() {
  if (!current) return;
  expression = current;
  fetch('/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ expression: current })
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      display.textContent = data.error;
      display.classList.add('error');
      justCalced = false;
    } else {
      exprEl.textContent = expression + ' =';
      current = String(data.result);
      display.textContent = current;
      display.classList.add('flash');
      setTimeout(() => display.classList.remove('flash'), 300);
      justCalced = true;
    }
  });
}

// Keyboard support
document.addEventListener('keydown', e => {
  if (e.key >= '0' && e.key <= '9') append(e.key);
  else if (e.key === '.') append('.');
  else if (e.key === '+') append('+');
  else if (e.key === '-') append('-');
  else if (e.key === '*') append('*');
  else if (e.key === '/') { e.preventDefault(); append('/'); }
  else if (e.key === '%') append('%');
  else if (e.key === '(') append('(');
  else if (e.key === ')') append(')');
  else if (e.key === 'Enter' || e.key === '=') calculate();
  else if (e.key === 'Backspace') deleteLast();
  else if (e.key === 'Escape') clearAll();
});
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get('expression', '')
    
    try:
        # Safe evaluation with math functions
        safe_dict = {
            '__builtins__': {},
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'abs': abs,
            'pi': math.pi,
            'e': math.e,
        }
        result = eval(expr, safe_dict)
        # Format nicely
        if isinstance(result, float):
            if result == int(result) and abs(result) < 1e15:
                result = int(result)
            else:
                result = round(result, 10)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'DIV BY ZERO'})
    except Exception as ex:
        return jsonify({'error': 'SYNTAX ERROR'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
