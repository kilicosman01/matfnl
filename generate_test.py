import json
import os

with open(r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\questions_data.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

limit_answers = ['D','C','D','C','E','E','A','C','B','B',
                 'D','B','B','E','B','B','B','E','A','C',
                 'D','C','B','E','D','A','A','B','D','B',
                 'E','B','D','B','C','E','E','C','B','B',
                 'A','C','B','C','E','A','C','A','E','B']

turev_answers = ['A','B','B','A','A','E','B','A','B','A',
                 'B','B','A','D','C','E','E','E','C','B',
                 'B','E','A','E','C','A','E','B','D','A',
                 'A','D','C','E','D','B','C','B','B','C',
                 'D','C','D','A','E','E','D','A','E','C',
                 'C','A','D','B','A','B','E','C','D','A',
                 'E','E','B','C','E','B','A','C','A','D',
                 'B','E','C','B','C','C','B','D','E','C',
                 'E','E','D','E','B','E','C','D','A','B',
                 'D','B','B','B','D','B','D','D','E','B']

integral_answers = ['A','D','E','C','E','D','E','A','B','A',
                    'C','C','E','B','A','D','C','A','A','C',
                    'E','C','B','C','B','D','C','C','D','B',
                    'B','A','C','E','D','B','B','D','A','B',
                    'E','A','C','A','C','C','D','B','E','A']

def build_questions_js(section, answers):
    questions = all_questions[section]
    items = []
    for i, ans in enumerate(answers):
        qnum = str(i + 1)
        if qnum in questions:
            img_data = f"data:image/png;base64,{questions[qnum]}"
            items.append(f'{{n:{i+1},ans:"{ans}",img:"{img_data}"}}')
        else:
            items.append(f'{{n:{i+1},ans:"{ans}",img:""}}')
    return '[' + ',\n'.join(items) + ']'

print("Building JS arrays...")
limit_js = build_questions_js('limit', limit_answers)
turev_js = build_questions_js('turev', turev_answers)
integral_js = build_questions_js('integral', integral_answers)
print("JS arrays built.")

html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Matematik II - İnteraktif Test Sistemi</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {{
  --bg: #0f1117;
  --surface: #1a1d2e;
  --surface2: #242740;
  --border: #2e3250;
  --accent: #6c63ff;
  --accent2: #a78bfa;
  --correct: #10b981;
  --wrong: #ef4444;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --radius: 14px;
}}

* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}

/* === HERO === */
.hero {{
  background: linear-gradient(135deg, #1a1d2e 0%, #0f1117 60%, #1a1d2e 100%);
  border-bottom: 1px solid var(--border);
  padding: 28px 24px 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
}}
.hero::before {{
  content:'';
  position:absolute; top:-50%; left:50%; transform:translateX(-50%);
  width:700px; height:700px;
  background:radial-gradient(circle,rgba(108,99,255,.1) 0%,transparent 65%);
  pointer-events:none;
}}
.hero h1 {{
  font-size:1.9rem; font-weight:800;
  background:linear-gradient(135deg,#6c63ff,#a78bfa,#60a5fa);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  margin-bottom:6px; position:relative;
}}
.hero p {{ color:var(--text-muted); font-size:.9rem; position:relative; }}

/* === GLOBAL SCORE === */
.score-bar {{
  background:var(--surface); border-bottom:1px solid var(--border);
  padding:10px 20px; display:flex; align-items:center; justify-content:center;
  gap:16px; flex-wrap:wrap;
}}
.chip {{
  display:flex; align-items:center; gap:6px;
  background:var(--surface2); padding:7px 14px; border-radius:50px;
  font-size:.82rem; font-weight:600;
}}
.chip.c {{ border:1px solid var(--correct); color:var(--correct); }}
.chip.w {{ border:1px solid var(--wrong); color:var(--wrong); }}
.chip.t {{ border:1px solid var(--accent); color:var(--accent2); }}

/* === TABS === */
.tabs {{
  display:flex; justify-content:center; gap:10px; padding:20px; flex-wrap:wrap;
}}
.tab-btn {{
  display:flex; align-items:center; gap:8px; padding:12px 22px;
  border-radius:50px; border:2px solid var(--border);
  background:var(--surface); color:var(--text-muted);
  font-family:'Inter',sans-serif; font-size:.9rem; font-weight:600; cursor:pointer;
  transition:all .3s;
}}
.tab-btn:hover {{ border-color:var(--accent); color:var(--accent2); transform:translateY(-2px); box-shadow:0 6px 20px rgba(108,99,255,.2); }}
.tab-btn.active {{ background:linear-gradient(135deg,var(--accent),#7c3aed); border-color:transparent; color:white; box-shadow:0 6px 20px rgba(108,99,255,.35); transform:translateY(-2px); }}
.qcount {{ background:rgba(255,255,255,.15); padding:2px 8px; border-radius:20px; font-size:.78rem; }}

/* === CONTAINER === */
.container {{ max-width:780px; margin:0 auto; padding:0 16px 60px; }}

.section {{ display:none; }}
.section.active {{ display:block; }}

/* === SECTION HEADER === */
.sec-header {{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:14px 18px; margin:16px 0 12px;
  display:flex; align-items:center; gap:14px;
}}
.sec-info {{ flex:1; }}
.sec-title {{ font-size:.95rem; font-weight:700; margin-bottom:5px; }}
.prog-bg {{ background:var(--surface2); border-radius:6px; height:5px; overflow:hidden; }}
.prog-fill {{ height:100%; background:linear-gradient(90deg,var(--accent),var(--accent2)); border-radius:6px; transition:width .4s ease; }}
.sec-stat {{ font-size:.8rem; color:var(--text-muted); white-space:nowrap; }}
.sec-stat strong {{ color:var(--text); }}

/* === QUESTION CARD === */
.q-card {{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  overflow:hidden; margin-bottom:12px;
  transition:border-color .3s, box-shadow .3s;
}}
.q-card.correct {{ border-color:var(--correct); box-shadow:0 0 0 1px rgba(16,185,129,.2); }}
.q-card.wrong {{ border-color:var(--wrong); box-shadow:0 0 0 1px rgba(239,68,68,.2); }}

.q-img-wrap {{ background:#fff; line-height:0; }}
.q-img-wrap img {{ width:100%; height:auto; display:block; }}

.q-footer {{
  display:flex; align-items:center; gap:8px;
  padding:10px 14px; border-top:1px solid var(--border);
  background:var(--surface2);
}}
.q-label {{ font-weight:700; font-size:.85rem; color:var(--accent2); min-width:26px; }}
.ans-row {{ display:flex; gap:6px; flex-wrap:wrap; }}
.ans-btn {{
  width:36px; height:36px; border-radius:8px; border:2px solid var(--border);
  background:transparent; color:var(--text);
  font-family:'Inter',sans-serif; font-weight:700; font-size:.88rem;
  cursor:pointer; transition:all .2s;
}}
.ans-btn:hover:not(:disabled) {{ border-color:var(--accent); color:var(--accent2); transform:scale(1.12); }}
.ans-btn.sel-correct {{ background:var(--correct)!important; border-color:var(--correct)!important; color:#fff!important; }}
.ans-btn.sel-wrong {{ background:var(--wrong)!important; border-color:var(--wrong)!important; color:#fff!important; animation:shake .4s; }}
.ans-btn.show-correct {{ border-color:var(--correct)!important; color:var(--correct)!important; font-weight:800; }}
.ans-btn:disabled {{ cursor:default; }}
.result-ico {{ margin-left:auto; font-size:1rem; }}

@keyframes shake {{
  0%,100% {{ transform:translateX(0); }}
  25% {{ transform:translateX(-4px); }}
  75% {{ transform:translateX(4px); }}
}}

/* === SUMMARY === */
.summary {{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:28px; text-align:center; margin:16px 0; display:none;
}}
.summary.active {{ display:block; }}
.summary h2 {{
  font-size:1.5rem; font-weight:800; margin-bottom:6px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.summary p.sub {{ color:var(--text-muted); font-size:.9rem; margin-bottom:24px; }}
.score-grid {{
  display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px;
}}
.sbox {{
  background:var(--surface2); border-radius:10px; padding:18px 12px; border:1px solid var(--border);
}}
.sbox.c {{ border-color:rgba(16,185,129,.4); }}
.sbox.w {{ border-color:rgba(239,68,68,.4); }}
.sbox.t {{ border-color:rgba(108,99,255,.4); }}
.sbox .lbl {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--text-muted); margin-bottom:5px; }}
.sbox .val {{ font-size:1.8rem; font-weight:800; }}
.sbox.c .val {{ color:var(--correct); }}
.sbox.w .val {{ color:var(--wrong); }}
.sbox.t .val {{ color:var(--accent2); }}
.sbox .pct {{ font-size:.75rem; color:var(--text-muted); margin-top:2px; }}
.act-btns {{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }}
.act-btn {{
  display:flex; align-items:center; gap:7px; padding:12px 24px;
  border-radius:10px; border:2px solid; font-family:'Inter',sans-serif;
  font-weight:700; font-size:.9rem; cursor:pointer; transition:all .3s;
}}
.act-btn.retry {{ background:linear-gradient(135deg,#ef4444,#dc2626); border-color:transparent; color:#fff; box-shadow:0 4px 14px rgba(239,68,68,.3); }}
.act-btn.retry:hover {{ transform:translateY(-2px); box-shadow:0 7px 20px rgba(239,68,68,.4); }}
.act-btn.restart {{ background:transparent; border-color:var(--border); color:var(--text-muted); }}
.act-btn.restart:hover {{ border-color:var(--accent); color:var(--accent2); transform:translateY(-2px); }}

/* === RETRY BANNER === */
.retry-banner {{
  background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.3);
  border-radius:10px; padding:10px 16px; text-align:center;
  font-size:.87rem; color:#fca5a5; margin:12px 0; display:none;
}}
.retry-banner.active {{ display:block; }}

/* === FINISH BTN === */
.finish-btn-wrap {{ text-align:center; padding:8px 0 20px; display:none; }}
.finish-btn-wrap.active {{ display:block; }}
.finish-btn {{
  padding:13px 32px; border-radius:10px;
  background:linear-gradient(135deg,var(--accent),#7c3aed);
  border:none; color:#fff; font-family:'Inter',sans-serif;
  font-size:.95rem; font-weight:700; cursor:pointer;
  box-shadow:0 4px 16px rgba(108,99,255,.35); transition:all .3s;
}}
.finish-btn:hover {{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(108,99,255,.4); }}

::-webkit-scrollbar {{ width:5px; }}
::-webkit-scrollbar-track {{ background:var(--bg); }}
::-webkit-scrollbar-thumb {{ background:var(--surface2); border-radius:3px; }}

@media(max-width:600px) {{
  .hero h1 {{ font-size:1.4rem; }}
  .score-grid {{ grid-template-columns:repeat(3,1fr); }}
  .sbox .val {{ font-size:1.5rem; }}
}}
</style>
</head>
<body>

<div class="hero">
  <h1>📐 Matematik II Test Sistemi</h1>
  <p>Limit &amp; Süreklilik · Türev · İntegral Alma — Soru başına işaretleme</p>
</div>

<div class="score-bar">
  <div class="chip t">📊 Toplam: <strong id="gTotal">0</strong></div>
  <div class="chip c">✅ Doğru: <strong id="gCorrect">0</strong></div>
  <div class="chip w">❌ Yanlış: <strong id="gWrong">0</strong></div>
</div>

<div class="tabs">
  <button class="tab-btn active" onclick="switchSection('limit')" id="tab-limit">
    <span>📏</span> Limit ve Süreklilik <span class="qcount">50 Soru</span>
  </button>
  <button class="tab-btn" onclick="switchSection('turev')" id="tab-turev">
    <span>📈</span> Türev <span class="qcount">100 Soru</span>
  </button>
  <button class="tab-btn" onclick="switchSection('integral')" id="tab-integral">
    <span>∫</span> İntegral Alma <span class="qcount">50 Soru</span>
  </button>
</div>

<div class="container">

<!-- LIMIT -->
<div class="section active" id="sec-limit">
  <div class="sec-header">
    <div class="sec-info">
      <div class="sec-title">📏 Limit ve Süreklilik</div>
      <div class="prog-bg"><div class="prog-fill" id="prog-limit" style="width:0"></div></div>
    </div>
    <div class="sec-stat"><strong id="ans-limit">0</strong>/50 yanıt</div>
  </div>
  <div class="retry-banner" id="retry-limit">🔴 <strong>Yanlış Yapılan Sorular</strong> — sadece hatalı cevaplarınız gösteriliyor</div>
  <div id="qs-limit"></div>
  <div class="finish-btn-wrap" id="finishwrap-limit">
    <button class="finish-btn" onclick="showSummary('limit')">📊 Sonuçları Gör</button>
  </div>
  <div class="summary" id="sum-limit">
    <h2>🎉 Limit Testi Tamamlandı!</h2>
    <p class="sub">İşte performansınız:</p>
    <div class="score-grid">
      <div class="sbox c"><div class="lbl">✅ Doğru</div><div class="val" id="lC">0</div><div class="pct" id="lCp"></div></div>
      <div class="sbox w"><div class="lbl">❌ Yanlış</div><div class="val" id="lW">0</div><div class="pct" id="lWp"></div></div>
      <div class="sbox t"><div class="lbl">📊 Puan</div><div class="val" id="lS">—</div><div class="pct" id="lSp">başarı</div></div>
    </div>
    <div class="act-btns">
      <button class="act-btn retry" onclick="retryWrong('limit')">🔁 Yanlışları Tekrar Çöz</button>
      <button class="act-btn restart" onclick="restartTest('limit')">↺ Baştan Başlat</button>
    </div>
  </div>
</div>

<!-- TÜREV -->
<div class="section" id="sec-turev">
  <div class="sec-header">
    <div class="sec-info">
      <div class="sec-title">📈 Türev</div>
      <div class="prog-bg"><div class="prog-fill" id="prog-turev" style="width:0"></div></div>
    </div>
    <div class="sec-stat"><strong id="ans-turev">0</strong>/100 yanıt</div>
  </div>
  <div class="retry-banner" id="retry-turev">🔴 <strong>Yanlış Yapılan Sorular</strong> — sadece hatalı cevaplarınız gösteriliyor</div>
  <div id="qs-turev"></div>
  <div class="finish-btn-wrap" id="finishwrap-turev">
    <button class="finish-btn" onclick="showSummary('turev')">📊 Sonuçları Gör</button>
  </div>
  <div class="summary" id="sum-turev">
    <h2>🎉 Türev Testi Tamamlandı!</h2>
    <p class="sub">İşte performansınız:</p>
    <div class="score-grid">
      <div class="sbox c"><div class="lbl">✅ Doğru</div><div class="val" id="tC">0</div><div class="pct" id="tCp"></div></div>
      <div class="sbox w"><div class="lbl">❌ Yanlış</div><div class="val" id="tW">0</div><div class="pct" id="tWp"></div></div>
      <div class="sbox t"><div class="lbl">📊 Puan</div><div class="val" id="tS">—</div><div class="pct" id="tSp">başarı</div></div>
    </div>
    <div class="act-btns">
      <button class="act-btn retry" onclick="retryWrong('turev')">🔁 Yanlışları Tekrar Çöz</button>
      <button class="act-btn restart" onclick="restartTest('turev')">↺ Baştan Başlat</button>
    </div>
  </div>
</div>

<!-- İNTEGRAL -->
<div class="section" id="sec-integral">
  <div class="sec-header">
    <div class="sec-info">
      <div class="sec-title">∫ İntegral Alma</div>
      <div class="prog-bg"><div class="prog-fill" id="prog-integral" style="width:0"></div></div>
    </div>
    <div class="sec-stat"><strong id="ans-integral">0</strong>/50 yanıt</div>
  </div>
  <div class="retry-banner" id="retry-integral">🔴 <strong>Yanlış Yapılan Sorular</strong> — sadece hatalı cevaplarınız gösteriliyor</div>
  <div id="qs-integral"></div>
  <div class="finish-btn-wrap" id="finishwrap-integral">
    <button class="finish-btn" onclick="showSummary('integral')">📊 Sonuçları Gör</button>
  </div>
  <div class="summary" id="sum-integral">
    <h2>🎉 İntegral Testi Tamamlandı!</h2>
    <p class="sub">İşte performansınız:</p>
    <div class="score-grid">
      <div class="sbox c"><div class="lbl">✅ Doğru</div><div class="val" id="iC">0</div><div class="pct" id="iCp"></div></div>
      <div class="sbox w"><div class="lbl">❌ Yanlış</div><div class="val" id="iW">0</div><div class="pct" id="iWp"></div></div>
      <div class="sbox t"><div class="lbl">📊 Puan</div><div class="val" id="iS">—</div><div class="pct" id="iSp">başarı</div></div>
    </div>
    <div class="act-btns">
      <button class="act-btn retry" onclick="retryWrong('integral')">🔁 Yanlışları Tekrar Çöz</button>
      <button class="act-btn restart" onclick="restartTest('integral')">↺ Baştan Başlat</button>
    </div>
  </div>
</div>

</div><!-- container -->

<script>
const LIMIT_QS  = {limit_js};
const TUREV_QS  = {turev_js};
const INTEGRAL_QS = {integral_js};

const TESTS = {{
  limit:    {{ qs: LIMIT_QS,    total:50,  prefix:'l' }},
  turev:    {{ qs: TUREV_QS,   total:100, prefix:'t' }},
  integral: {{ qs: INTEGRAL_QS, total:50,  prefix:'i' }}
}};

const state = {{
  limit:    {{ answered:{{}}, retryMode:false, retryIds:[] }},
  turev:    {{ answered:{{}}, retryMode:false, retryIds:[] }},
  integral: {{ answered:{{}}, retryMode:false, retryIds:[] }}
}};

// ---- BUILD QUESTION CARDS ----
function buildCards(test, qList, container) {{
  container.innerHTML = '';
  qList.forEach(q => {{
    const card = document.createElement('div');
    card.className = 'q-card';
    card.id = `qcard-${{test}}-${{q.n}}`;

    if (q.img) {{
      const imgWrap = document.createElement('div');
      imgWrap.className = 'q-img-wrap';
      const img = document.createElement('img');
      img.src = q.img;
      img.alt = `Soru ${{q.n}}`;
      img.loading = 'lazy';
      imgWrap.appendChild(img);
      card.appendChild(imgWrap);
    }}

    const footer = document.createElement('div');
    footer.className = 'q-footer';

    const lbl = document.createElement('div');
    lbl.className = 'q-label';
    lbl.textContent = `${{q.n}}.`;
    footer.appendChild(lbl);

    const row = document.createElement('div');
    row.className = 'ans-row';
    ['A','B','C','D','E'].forEach(letter => {{
      const btn = document.createElement('button');
      btn.className = 'ans-btn';
      btn.id = `btn-${{test}}-${{q.n}}-${{letter}}`;
      btn.textContent = letter;
      btn.onclick = () => answer(test, q.n, letter, q.ans);
      row.appendChild(btn);
    }});
    footer.appendChild(row);

    const ico = document.createElement('div');
    ico.className = 'result-ico';
    ico.id = `ico-${{test}}-${{q.n}}`;
    footer.appendChild(ico);

    card.appendChild(footer);
    container.appendChild(card);
  }});
}}

function init() {{
  ['limit','turev','integral'].forEach(test => {{
    const container = document.getElementById('qs-' + test);
    buildCards(test, TESTS[test].qs, container);
  }});
  updateGlobal();
}}

// ---- ANSWER ----
function answer(test, qNum, letter, correct) {{
  const st = state[test];
  if (st.answered[qNum]) return;

  const isCorrect = letter === correct;
  st.answered[qNum] = {{ chosen: letter, correct: correct, isCorrect: isCorrect }};

  // Disable all buttons for this question
  ['A','B','C','D','E'].forEach(l => {{
    const b = document.getElementById(`btn-${{test}}-${{qNum}}-${{l}}`);
    if (b) b.disabled = true;
  }});

  const chosenBtn = document.getElementById(`btn-${{test}}-${{qNum}}-${{letter}}`);
  const card = document.getElementById(`qcard-${{test}}-${{qNum}}`);
  const ico = document.getElementById(`ico-${{test}}-${{qNum}}`);

  if (isCorrect) {{
    chosenBtn.classList.add('sel-correct');
    card.classList.add('correct');
    ico.textContent = '✅';
  }} else {{
    chosenBtn.classList.add('sel-wrong');
    card.classList.add('wrong');
    ico.textContent = '❌';
    const corrBtn = document.getElementById(`btn-${{test}}-${{qNum}}-${{correct}}`);
    if (corrBtn) corrBtn.classList.add('show-correct');
  }}

  updateProgress(test);
  updateGlobal();
  checkFinish(test);
}}

// ---- PROGRESS ----
function updateProgress(test) {{
  const st = state[test];
  const total = TESTS[test].total;
  const answered = Object.keys(st.answered).length;
  const pct = (answered / total) * 100;
  document.getElementById('prog-' + test).style.width = pct + '%';
  document.getElementById('ans-' + test).textContent = answered;
}}

function updateGlobal() {{
  let tot=0, cor=0, wr=0;
  ['limit','turev','integral'].forEach(t => {{
    Object.values(state[t].answered).forEach(a => {{
      tot++; if(a.isCorrect) cor++; else wr++;
    }});
  }});
  document.getElementById('gTotal').textContent = tot;
  document.getElementById('gCorrect').textContent = cor;
  document.getElementById('gWrong').textContent = wr;
}}

function checkFinish(test) {{
  const st = state[test];
  const total = TESTS[test].total;
  const answered = Object.keys(st.answered).length;
  if (answered === total) {{
    document.getElementById('finishwrap-' + test).classList.add('active');
  }}
}}

// ---- SWITCH SECTION ----
function switchSection(test) {{
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('sec-' + test).classList.add('active');
  document.getElementById('tab-' + test).classList.add('active');
}}

// ---- SUMMARY ----
function showSummary(test) {{
  const st = state[test];
  let cor=0, wr=0;
  Object.values(st.answered).forEach(a => {{ if(a.isCorrect) cor++; else wr++; }});
  const total = cor + wr;
  const pct = total > 0 ? Math.round((cor/total)*100) : 0;

  const prefix = TESTS[test].prefix;
  document.getElementById(prefix+'C').textContent = cor;
  document.getElementById(prefix+'W').textContent = wr;
  document.getElementById(prefix+'S').textContent = pct + '%';
  document.getElementById(prefix+'Cp').textContent = total > 0 ? Math.round((cor/total)*100) + '%' : '';
  document.getElementById(prefix+'Wp').textContent = total > 0 ? Math.round((wr/total)*100) + '%' : '';

  document.getElementById('finishwrap-' + test).classList.remove('active');
  document.getElementById('sum-' + test).classList.add('active');
  document.getElementById('sum-' + test).scrollIntoView({{behavior:'smooth', block:'start'}});
  updateGlobal();
}}

// ---- RETRY WRONG ----
function retryWrong(test) {{
  const st = state[test];
  const wrongNums = Object.entries(st.answered)
    .filter(([,a]) => !a.isCorrect)
    .map(([n]) => parseInt(n));

  if (wrongNums.length === 0) {{
    alert('Tebrikler! Hiç yanlış cevabınız yok!');
    return;
  }}

  // Reset wrong answers from state
  wrongNums.forEach(n => delete st.answered[n]);
  st.retryMode = true;
  st.retryIds = wrongNums;

  // Filter questions to only wrong ones
  const allQs = TESTS[test].qs;
  const retryQs = allQs.filter(q => wrongNums.includes(q.n));

  // Rebuild only retry cards
  const container = document.getElementById('qs-' + test);
  buildCards(test, retryQs, container);

  // Re-apply correct answers state to non-retry questions (not needed since we only show retry cards)
  // But we need to restore the correct answers' visual state won't matter since we rebuilt

  document.getElementById('sum-' + test).classList.remove('active');
  document.getElementById('finishwrap-' + test).classList.remove('active');
  document.getElementById('retry-' + test).classList.add('active');

  updateProgress(test);
  updateGlobal();
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

// ---- RESTART ----
function restartTest(test) {{
  const st = state[test];
  st.answered = {{}};
  st.retryMode = false;
  st.retryIds = [];

  const container = document.getElementById('qs-' + test);
  buildCards(test, TESTS[test].qs, container);

  document.getElementById('sum-' + test).classList.remove('active');
  document.getElementById('finishwrap-' + test).classList.remove('active');
  document.getElementById('retry-' + test).classList.remove('active');
  document.getElementById('prog-' + test).style.width = '0';
  document.getElementById('ans-' + test).textContent = '0';

  updateGlobal();
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

init();
</script>
</body>
</html>"""

output = r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\Matematik_II_Test.html'
with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

size_mb = os.path.getsize(output) / 1024 / 1024
print(f"HTML olusturuldu: {output}")
print(f"Boyut: {size_mb:.1f} MB")
