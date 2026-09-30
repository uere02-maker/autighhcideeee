import os
import secrets

# Configurações do Servidor
PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = secrets.token_hex(32)

# Configurações do Bot / Interface
MUSIC = "https://www.youtube.com/embed/5KWGKVF3aD8?autoplay=1&loop=1&playlist=5KWGKVF3aD8&controls=0&disablekb=1&modestbranding=1&rel=0&showinfo=0&fs=0&iv_load_policy=3"

# Constantes de Estilo
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
    :root{--bg:#0a0a12;--s1:#111122;--s2:#181830;--b:#252545;--p:#ff6b35;--su:#00e676;--d:#ff3355;--w:#ffaa00;--a:#9944ff;--t:#e8e8f5;--t2:#8888bb;--t3:#555588}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--t);min-height:100vh;background-image:radial-gradient(ellipse at 20% 50%,rgba(255,107,53,.04) 0%,transparent 55%);background-attachment:fixed}
    .app{max-width:1000px;margin:0 auto;padding:20px;position:relative;z-index:1}
    .header{text-align:center;padding:35px 20px 25px;position:relative}
    .header::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:250px;height:250px;background:radial-gradient(circle,rgba(255,107,53,.08) 0%,transparent 70%);pointer-events:none}
    .logo{font-family:'Orbitron',sans-serif;font-size:2.5em;font-weight:900;letter-spacing:4px;background:linear-gradient(135deg,#ff6b35,#ffaa00,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;z-index:1;animation:glow 2s ease-in-out infinite alternate}
    @keyframes glow{from{filter:brightness(1)}to{filter:brightness(1.3)}}
    .subtitle{font-family:'JetBrains Mono',monospace;color:var(--t3);letter-spacing:3px;font-size:.85em;margin-top:10px}
    .badge-row{display:flex;justify-content:center;gap:10px;margin-top:15px;flex-wrap:wrap}
    .badge{padding:6px 16px;border-radius:20px;font-size:.75em;font-weight:600;letter-spacing:1px}
    .badge-p{background:rgba(255,107,53,.15);color:var(--p);border:1px solid rgba(255,107,53,.3)}
    .badge-g{background:rgba(0,230,118,.15);color:var(--su);border:1px solid rgba(0,230,118,.3)}
    .badge-a{background:rgba(153,68,255,.15);color:var(--a);border:1px solid rgba(153,68,255,.3)}
    .card{background:var(--s2);border:1px solid var(--b);border-radius:16px;padding:28px;margin-bottom:20px;box-shadow:0 8px 32px rgba(0,0,0,.3)}
    .card-title{font-size:1.2em;font-weight:700;margin-bottom:8px;color:var(--p);display:flex;align-items:center;gap:10px}
    .card-desc{color:var(--t2);font-size:.85em;margin-bottom:20px}
    .form-group{margin-bottom:16px}
    .form-label{display:block;font-weight:600;margin-bottom:6px;color:var(--t2);font-size:.85em}
    .form-input,textarea{width:100%;padding:12px 16px;background:var(--bg);border:2px solid var(--b);border-radius:10px;color:var(--t);font-family:'JetBrains Mono',monospace;font-size:.85em;outline:none;transition:all .3s}
    .form-input:focus,textarea:focus{border-color:var(--p);box-shadow:0 0 0 4px rgba(255,107,53,.3)}
    textarea{min-height:200px;resize:vertical}
    .btn{padding:12px 24px;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-size:.9em;letter-spacing:1px;transition:all .3s;display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-family:'Inter',sans-serif}
    .btn-p{background:linear-gradient(135deg,#ff6b35,#ff4500);color:#fff;box-shadow:0 4px 20px rgba(255,107,53,.3)}
    .btn-p:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(255,107,53,.3)}
    .btn-s{background:linear-gradient(135deg,var(--su),#00c853);color:#000}
    .btn-block{width:100%;justify-content:center}
    .code-block{background:#000;border:1px solid var(--b);border-radius:10px;padding:20px;font-family:'JetBrains Mono',monospace;color:#00ff88;overflow-x:auto;white-space:pre-wrap;max-height:500px;overflow-y:auto;font-size:.8em;line-height:1.5}
    .alert{padding:14px 18px;border-radius:10px;margin:14px 0;font-weight:500;display:flex;align-items:center;gap:10px}
    .alert-s{background:rgba(0,230,118,.1);border:1px solid rgba(0,230,118,.3);color:var(--su)}
    .alert-e{background:rgba(255,51,85,.1);border:1px solid rgba(255,51,85,.3);color:var(--d)}
    .alert-i{background:rgba(255,107,53,.1);border:1px solid rgba(255,107,53,.3);color:var(--p)}
    @media(max-width:768px){.logo{font-size:2em}.card{padding:18px}}
</style>
"""
