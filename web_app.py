#!/usr/bin/env python3
"""
2M Code Web UI — Sleek Single-Page Web IDE

A dark-themed, single-page web interface for the 2M Code AI coding assistant.
Connects directly into the orchestrator/core loop.

Usage:
    python web_app.py
    # Opens at http://localhost:5000
"""

from __future__ import annotations

import json
import os
import sys
import uuid
import time
import logging
from pathlib import Path

import litellm
from flask import Flask, render_template_string, request, Response, jsonify, session
from dotenv import load_dotenv

from core.config import load_config, save_config
from core.model_provider import get_litellm_kwargs, PROVIDERS
from core.ui import console
from orchestrator import build_system_prompt, process_llm_response
from execution.runner import extract_code_blocks

load_dotenv()

logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)
app.secret_key = os.urandom(32)

chat_histories: dict[str, list[dict]] = {}

# ---------------------------------------------------------------------------
# HTML Template — Embedded Single-Page Application
# ---------------------------------------------------------------------------

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>2M Code Web IDE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/dracula.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg-primary:#111;--bg-secondary:#1a1a1a;--bg-tertiary:#222;--border:#333;--text-primary:#e0e0e0;--text-secondary:#888;--accent:#4fd1c5;--accent-dim:rgba(79,209,197,0.12);--danger:#ef4444;--font-ui:'Inter',-apple-system,sans-serif;--font-code:'JetBrains Mono','Fira Code',monospace;--sidebar-w:250px;--chat-h:320px}
body{font-family:var(--font-ui);background:var(--bg-primary);color:var(--text-primary);overflow:hidden;height:100vh}
.grid{display:grid;grid-template-columns:var(--sidebar-w) 1fr;grid-template-rows:1fr var(--chat-h);height:100vh}
/* Sidebar */
.sidebar{grid-column:1;grid-row:1/3;background:var(--bg-secondary);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden}
.sidebar-hdr{padding:14px 16px;border-bottom:1px solid var(--border);font-size:11px;font-weight:600;letter-spacing:1px;color:var(--text-secondary);text-transform:uppercase}
.file-tree{flex:1;overflow-y:auto;padding:4px 0;font-size:13px}
.file-tree::-webkit-scrollbar{width:5px}
.file-tree::-webkit-scrollbar-track{background:transparent}
.file-tree::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.fi{padding:3px 16px;cursor:pointer;color:var(--text-secondary);display:flex;align-items:center;gap:6px;transition:all .12s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;user-select:none}
.fi:hover{background:var(--bg-tertiary);color:var(--text-primary)}
.fi.active{background:var(--accent-dim);color:var(--accent)}
.fi.dir{font-weight:500;color:var(--text-primary)}
.fi .ico{flex-shrink:0;width:16px;text-align:center;font-size:13px}
.fi .chv{font-size:9px;transition:transform .12s;width:12px}
.fi .chv.open{transform:rotate(90deg)}
/* Main content */
.main{grid-column:2;grid-row:1;background:var(--bg-primary);display:flex;flex-direction:column;overflow:hidden;min-height:0}
.ed-hdr{padding:8px 16px;border-bottom:1px solid var(--border);font-size:12px;color:var(--text-secondary);font-family:var(--font-code);display:flex;align-items:center;gap:8px;flex-shrink:0}
.ed-body{flex:1;overflow:auto;font-family:var(--font-code);font-size:13px;line-height:1.6;min-height:0}
.ed-body::-webkit-scrollbar{width:6px}
.ed-body::-webkit-scrollbar-track{background:transparent}
.ed-body::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.ed-body pre{padding:20px;margin:0;background:transparent!important}
.ed-body code{font-family:var(--font-code)!important;background:transparent!important;font-size:13px}
.ed-ph{display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-secondary);font-family:var(--font-ui);font-size:14px;text-align:center;flex-direction:column;gap:12px;padding:40px}
.ed-ph .lg{font-size:28px;font-weight:700;color:var(--accent);font-family:var(--font-code);letter-spacing:4px;opacity:.7}
.ed-ph .sub{font-size:13px;color:var(--text-secondary)}
/* Chat */
.chat{grid-column:2;grid-row:2;background:var(--bg-secondary);border-top:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;min-height:0}
.chat-hdr{padding:6px 16px;border-bottom:1px solid var(--border);font-size:11px;font-weight:600;letter-spacing:1px;color:var(--text-secondary);text-transform:uppercase;flex-shrink:0;display:flex;align-items:center;justify-content:space-between}
.chat-bdg{font-size:10px;color:var(--accent);background:var(--accent-dim);padding:2px 8px;border-radius:4px;font-weight:400;letter-spacing:0;text-transform:none;font-family:var(--font-code);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chat-msgs{flex:1;overflow-y:auto;padding:10px 16px;font-size:13px;line-height:1.6;min-height:0}
.chat-msgs::-webkit-scrollbar{width:5px}
.chat-msgs::-webkit-scrollbar-track{background:transparent}
.chat-msgs::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.msg{margin-bottom:10px;animation:fadeIn .18s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.msg.user{text-align:right}
.msg.user .bbl{background:var(--accent-dim);color:var(--accent);display:inline-block;padding:7px 13px;border-radius:10px 10px 3px 10px;max-width:78%;text-align:left;border:1px solid rgba(79,209,197,.18);font-size:13px}
.msg.assist .bbl{color:var(--text-primary);max-width:100%}
.msg.assist .bbl p{margin:5px 0}
.msg.assist .bbl pre{background:var(--bg-tertiary);border:1px solid var(--border);border-radius:6px;padding:10px 12px;margin:6px 0;overflow-x:auto;font-size:12px;line-height:1.5}
.msg.assist .bbl code{font-family:var(--font-code);font-size:12px}
.msg.assist .bbl pre code{background:transparent;padding:0}
.msg.assist .bbl :not(pre)>code{background:var(--bg-tertiary);padding:1px 5px;border-radius:3px;font-size:12px;color:var(--accent)}
.msg.assist .bbl ul,.msg.assist .bbl ol{padding-left:20px;margin:4px 0}
.msg.assist .bbl h1,.msg.assist .bbl h2,.msg.assist .bbl h3,.msg.assist .bbl h4{color:var(--accent);margin:8px 0 4px}
.msg.assist .bbl hr{border:none;border-top:1px solid var(--border);margin:8px 0}
.msg.assist .bbl blockquote{border-left:3px solid var(--accent);padding-left:10px;color:var(--text-secondary);margin:6px 0}
.chat-inp{padding:8px 16px;border-top:1px solid var(--border);display:flex;gap:6px;flex-shrink:0}
.chat-inp input{flex:1;background:var(--bg-tertiary);border:1px solid var(--border);border-radius:6px;padding:9px 12px;color:var(--text-primary);font-family:var(--font-code);font-size:13px;outline:none;transition:border-color .15s}
.chat-inp input:focus{border-color:var(--accent)}
.chat-inp input::placeholder{color:#555}
.chat-inp button{background:var(--accent);color:#111;border:none;border-radius:6px;padding:9px 14px;font-size:15px;cursor:pointer;transition:all .15s;font-weight:600;line-height:1}
.chat-inp button:hover{opacity:.9}
.chat-inp button:disabled{opacity:.35;cursor:not-allowed}
.chat-st{display:flex;justify-content:space-between;padding:2px 16px;font-size:10px;color:var(--text-secondary);font-family:var(--font-code);border-top:1px solid var(--border);flex-shrink:0}
.chat-st .err{color:var(--danger)}
/* Typing */
.typing{display:flex;gap:3px;padding:6px 0;align-items:center;color:var(--text-secondary);font-size:11px;font-family:var(--font-ui)}
.typing .dot{width:5px;height:5px;border-radius:50%;background:var(--text-secondary);animation:pulse 1.2s infinite}
.typing .dot:nth-child(2){animation-delay:.2s}
.typing .dot:nth-child(3){animation-delay:.4s}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}
/* Settings overlay */
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center}
.overlay.open{display:flex}
.overlay-box{background:var(--bg-secondary);border:1px solid var(--border);border-radius:12px;padding:24px;width:480px;max-height:80vh;overflow-y:auto}
.overlay-box h2{color:var(--accent);font-size:16px;font-weight:600;margin-bottom:16px}
.overlay-box label{display:block;font-size:12px;color:var(--text-secondary);margin:10px 0 4px;font-weight:500}
.overlay-box select,.overlay-box input[type=text]{width:100%;background:var(--bg-tertiary);border:1px solid var(--border);border-radius:6px;padding:8px 10px;color:var(--text-primary);font-size:13px;font-family:var(--font-code);outline:none}
.overlay-box select:focus,.overlay-box input[type=text]:focus{border-color:var(--accent)}
.overlay-box .btn-row{display:flex;gap:8px;margin-top:16px;justify-content:flex-end}
.overlay-box .btn-row button{padding:8px 16px;border-radius:6px;border:none;font-size:13px;font-weight:500;cursor:pointer;transition:all .12s}
.overlay-box .btn-row .btn-primary{background:var(--accent);color:#111}
.overlay-box .btn-row .btn-primary:hover{opacity:.9}
.overlay-box .btn-row .btn-ghost{background:transparent;color:var(--text-secondary);border:1px solid var(--border)}
.overlay-box .btn-row .btn-ghost:hover{background:var(--bg-tertiary)}
.fld{display:flex;flex-direction:column;gap:4px}
/* Responsive */
@media(max-width:768px){:root{--sidebar-w:0px;--chat-h:280px}.sidebar{display:none}}
</style>
</head>
<body>
<div class="grid">
  <aside class="sidebar">
    <div class="sidebar-hdr">&#x1F4C1;  Explorer</div>
    <div class="file-tree" id="fileTree"></div>
  </aside>
  <main class="main">
    <div class="ed-hdr"><span>&#x1F4C4;</span><span id="edFile">workspace / welcome</span></div>
    <div class="ed-body" id="edBody">
      <div class="ed-ph" id="edPh">
        <div class="lg">2 M &nbsp; C O D E</div>
        <div class="sub">AI-Powered Web IDE</div>
        <div class="sub" style="font-size:11px;margin-top:6px;color:#555">Ask the AI to generate code &mdash; results appear here</div>
      </div>
    </div>
  </main>
  <div class="chat">
    <div class="chat-hdr">
      <span>&#x1F4AC;  AI Chat  &nbsp;<span id="cmdHint" style="color:#555;font-weight:400;letter-spacing:0;text-transform:none;font-size:10px">/help</span></span>
      <span class="chat-bdg" id="modelBadge">loading...</span>
    </div>
    <div class="chat-msgs" id="chatMsgs"></div>
    <div class="chat-inp">
      <input type="text" id="chatInp" placeholder="Ask the AI to code something..." autofocus>
      <button id="sendBtn">&rarr;</button>
    </div>
    <div class="chat-st"><span id="stText">Ready</span><span id="stConn">&#x25CF; Connected</span></div>
  </div>
</div>

<!-- Settings Overlay -->
<div class="overlay" id="settingsOverlay">
  <div class="overlay-box">
    <h2>&#x2699;  Connection Settings</h2>
    <div class="fld">
      <label>Provider</label>
      <select id="selProvider"></select>
    </div>
    <div class="fld">
      <label>Model</label>
      <select id="selModel"></select>
    </div>
    <div class="fld">
      <label>API Key <span style="color:#555;font-weight:400">(leave blank to keep current)</span></label>
      <input type="text" id="inpApiKey" placeholder="sk-...">
    </div>
    <div class="fld">
      <label>API Base URL <span style="color:#555;font-weight:400">(optional)</span></label>
      <input type="text" id="inpApiBase" placeholder="https://...">
    </div>
    <div class="btn-row">
      <button class="btn-ghost" onclick="closeSettings()">Cancel</button>
      <button class="btn-primary" onclick="saveSettings()">Save &amp; Connect</button>
    </div>
    <div id="settingsStatus" style="margin-top:8px;font-size:12px;color:var(--accent)"></div>
  </div>
</div>

<script>
const $=(s)=>{const e=document.querySelector(s);if(!e)console.warn('el not found:',s);return e};
let streaming=false, curFile=null;

marked.setOptions({breaks:true,gfm:true});

document.addEventListener('DOMContentLoaded',()=>{loadFileTree();loadConfig();initChat()});

function initChat(){
  const inp=$('#chatInp'),btn=$('#sendBtn');
  inp.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg()}});
  btn.addEventListener('click',sendMsg);
  setTimeout(()=>inp.focus(),200);
}

// ── Config ──
async function loadConfig(){
  try{
    const r=await fetch('/api/config'),d=await r.json();
    $('#modelBadge').textContent=d.model||'unknown';
  }catch(e){$('#modelBadge').textContent='offline'}
}

// ── File Tree ──
async function loadFileTree(){
  try{
    const r=await fetch('/api/files'),d=await r.json();
    renderTree(d,$('#fileTree'),0);
  }catch(e){$('#fileTree').innerHTML='<div class="fi" style="color:#555;font-style:italic">Failed to load</div>'}
}

function renderTree(items,container,depth){
  if(!items||!items.length){container.innerHTML='<div class="fi" style="color:#555;font-style:italic">Empty workspace</div>';return}
  container.innerHTML='';
  items.forEach(item=>{
    const div=document.createElement('div');
    div.className='fi'+(item.type==='dir'?' dir':'');
    div.style.paddingLeft=(14+depth*14)+'px';
    if(item.type==='dir'){
      div.innerHTML='<span class="chv">&#x25B6;</span><span class="ico">&#x1F4C1;</span>'+item.name;
      div.addEventListener('click',()=>{
        const nxt=div.nextElementSibling;
        if(nxt&&nxt.classList.contains('fd')){
          nxt.style.display=nxt.style.display==='none'?'':'none';
          div.querySelector('.chv').classList.toggle('open');
        }
      });
      container.appendChild(div);
      if(item.children&&item.children.length){
        const cc=document.createElement('div');cc.className='fd';
        renderTree(item.children,cc,depth+1);
        container.appendChild(cc);
      }
    }else{
      const ext=item.name.split('.').pop().toLowerCase();
      const icons={py:'&#x1F40D;',js:'&#x1F4DC;',ts:'&#x1F4D8;',html:'&#x1F310;',css:'&#x1F3A8;',json:'&#x1F4CB;',md:'&#x1F4DD;',txt:'&#x1F4C4;',yml:'&#x2699;',yaml:'&#x2699;',toml:'&#x2699;',env:'&#x1F510;',gitignore:'&#x1F6E1;',cfg:'&#x2699;',ini:'&#x2699;',lock:'&#x1F512;',xml:'&#x1F4C4;',sh:'&#x1F4BB;',bat:'&#x1F4BB;',ps1:'&#x1F4BB;',sql:'&#x1F4CA;',md:'&#x1F4DD;',svg:'&#x1F5BC;',png:'&#x1F5BC;',jpg:'&#x1F5BC;',jpeg:'&#x1F5BC;',gif:'&#x1F5BC;',ico:'&#x1F5BC;'};
      const icon=icons[ext]||'&#x1F4C4;';
      div.innerHTML='<span class="ico">'+icon+'</span>'+item.name;
      div.addEventListener('click',()=>{
        document.querySelectorAll('.fi').forEach(el=>el.classList.remove('active'));
        div.classList.add('active');openFile(item.path);
      });
      container.appendChild(div);
    }
  });
}

async function openFile(path){
  curFile=path;
  $('#edFile').textContent=path.replace(/\\\\/g,'/');
  try{
    const r=await fetch('/api/files/'+encodeURIComponent(path));
    if(!r.ok)throw new Error('fail');
    const txt=await r.text(),ph=$('#edPh');
    if(ph)ph.style.display='none';
    const ext=path.split('.').pop().toLowerCase();
    const langMap={py:'python',js:'javascript',ts:'typescript',jsx:'javascript',tsx:'typescript',html:'html',css:'css',json:'json',md:'markdown',yml:'yaml',yaml:'yaml',xml:'xml',sh:'bash',bat:'dos',ps1:'powershell',sql:'sql',env:'bash',toml:'ini',ini:'ini',cfg:'ini',dockerfile:'dockerfile',lock:'json'};
    const lang=langMap[ext]||'plaintext';
    let esc=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    $('#edBody').innerHTML='<pre><code class="language-'+lang+'">'+esc+'</code></pre>';
    $('#edBody').querySelectorAll('pre code').forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
  }catch(e){
    $('#edBody').innerHTML='<div class="ed-ph"><div class="sub" style="color:#ef4444">Failed to load</div><div class="sub">'+path+'</div></div>';
  }
}

// ── Messages ──
function addMsg(role,content){
  const d=document.createElement('div');
  d.className='msg '+(role==='user'?'user':'assist');
  const b=document.createElement('div');b.className='bbl';
  if(role==='assist')b.innerHTML=marked.parse(content);
  else b.textContent=content;
  d.appendChild(b);
  $('#chatMsgs').appendChild(d);
  scrollChat();
}

function scrollChat(){const c=$('#chatMsgs');if(c)c.scrollTop=c.scrollHeight}

// ── Send ──
async function sendMsg(){
  const inp=$('#chatInp'),msg=inp.value.trim();
  if(!msg||streaming)return;
  inp.value='';streaming=true;$('#sendBtn').disabled=true;$('#stText').textContent='Thinking...';
  addMsg('user',msg);
  const td=document.createElement('div');td.className='typing';td.id='typi';
  td.innerHTML='<span style="font-size:10px">AI</span><div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  $('#chatMsgs').appendChild(td);scrollChat();
  if(msg.startsWith('/')){handleCmd(msg);return}
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
    const reader=r.body.getReader(),dec=new TextDecoder();
    let buf='';
    function read(){
      reader.read().then(({done,value})=>{
        if(done){
          streaming=false;$('#sendBtn').disabled=false;$('#stText').textContent='Ready';
          const t=document.getElementById('typi');if(t)t.remove();
          finMsg();scrollChat();return;
        }
        buf+=dec.decode(value,{stream:true});
        const lines=buf.split('\\n');buf=lines.pop()||'';
        for(const line of lines){
          if(!line.startsWith('data: '))continue;
          try{
            const d=JSON.parse(line.slice(6));
            if(d.token)appToken(d.token);
            else if(d.code){showCode(d.code)}
            else if(d.status&&d.status!==''){$('#stText').textContent=d.status}
            else if(d.error){errMsg(d.error)}
            else if(d.done){
              const t=document.getElementById('typi');if(t)t.remove();
              finMsg();
            }
          }catch(e){}
        }
        scrollChat();read();
      }).catch(e=>errMsg(e.message));
    }
    read();
  }catch(e){errMsg(e.message)}
  scrollChat();
}

function handleCmd(cmd){
  streaming=false;$('#sendBtn').disabled=false;$('#stText').textContent='Ready';
  const t=document.getElementById('typi');if(t)t.remove();
  if(cmd==='/help'){
    addMsg('assist','**2M Code Commands**\n\n`/help` — Show this help\n`/connect` — Open settings panel\n`/model <name>` — Switch model instantly\n`/clear` — Clear chat history');
    return;
  }
  if(cmd.startsWith('/model ')){
    const mn=cmd.slice(7).trim();
    if(!mn){addMsg('assist','Usage: `/model <model_name>`\nExample: `/model gpt-4o`');return}
    fetch('/api/model',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:mn})})
      .then(r=>r.json()).then(d=>{
        if(d.success){addMsg('assist','✅ Model switched to: `'+mn+'`');loadConfig()}
        else addMsg('assist','❌ Error: '+d.error);
      }).catch(e=>addMsg('assist','❌ Error: '+e.message));
    return;
  }
  if(cmd==='/connect'){
    $('#settingsOverlay').classList.add('open');
    loadSettingsForm();
    addMsg('assist','⚙️ Settings panel opened. Configure your provider and model above.');
    return;
  }
  if(cmd==='/clear'){
    fetch('/api/clear',{method:'POST'}).then(()=>{$('#chatMsgs').innerHTML='';addMsg('assist','🧹 Chat cleared.')});
    return;
  }
  addMsg('assist','❓ Unknown: `'+cmd+'`\nType `/help` for available commands.');
}

function appToken(token){
  let md=document.getElementById('strMsg');
  if(!md){
    md=document.createElement('div');md.className='msg assist';md.id='strMsg';
    const b=document.createElement('div');b.className='bbl';md.appendChild(b);
    $('#chatMsgs').appendChild(md);
  }
  md.querySelector('.bbl').innerHTML+=token;
}

function finMsg(){
  const md=document.getElementById('strMsg');
  if(!md)return;
  md.removeAttribute('id');
  const bbl=md.querySelector('.bbl'),raw=bbl.textContent;
  bbl.innerHTML=marked.parse(raw);
  bbl.querySelectorAll('pre code').forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
}

function showCode(code){
  const ph=$('#edPh');if(ph)ph.style.display='none';
  $('#edFile').textContent='AI Generated Code';
  let esc=code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  $('#edBody').innerHTML='<pre><code class="language-python">'+esc+'</code></pre>';
  $('#edBody').querySelectorAll('pre code').forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
}

function errMsg(e){
  streaming=false;$('#sendBtn').disabled=false;$('#stText').textContent='Error';
  const t=document.getElementById('typi');if(t)t.remove();
  addMsg('assist','❌ **Error:** '+e+'\n\nTry `/connect` to reconfigure or `/help` for commands.');
}

// ── Settings ──
async function loadSettingsForm(){
  try{
    const r=await fetch('/api/connect'),d=await r.json();
    const selP=$('#selProvider'),selM=$('#selModel');
    selP.innerHTML='';
    for(const[k,v]of Object.entries(d.providers||{})){
      const opt=document.createElement('option');opt.value=k;opt.textContent=v.label;
      if(k===d.provider)opt.selected=true;
      selP.appendChild(opt);
    }
    updateModels(selP.value,d);
    selP.addEventListener('change',()=>updateModels(selP.value,d));
    $('#inpApiKey').value='';
    $('#inpApiBase').value=d.api_base||'';
  }catch(e){$('#settingsStatus').textContent='Error loading settings';}
}

function updateModels(provider,data){
  const selM=$('#selModel');
  if(!selM)return;
  selM.innerHTML='';
  const p=data.providers[provider],cfg=data.model;
  if(p&&p.models){
    p.models.forEach(m=>{
      const opt=document.createElement('option');opt.value=m;opt.textContent=m;
      if(m===cfg)opt.selected=true;
      selM.appendChild(opt);
    });
  }
}

function closeSettings(){$('#settingsOverlay').classList.remove('open')}

async function saveSettings(){
  const body={provider:$('#selProvider').value,model:$('#selModel').value,api_key:$('#inpApiKey').value,api_base:$('#inpApiBase').value};
  $('#settingsStatus').textContent='Saving...';
  try{
    const r=await fetch('/api/connect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const d=await r.json();
    if(d.success){
      $('#settingsStatus').textContent='✅ Settings saved!';
      closeSettings();loadConfig();
      $('#chatMsgs').innerHTML='';
      addMsg('assist','✅ Configuration updated!\nProvider: `'+body.provider+'`\nModel: `'+body.model+'`');
    }else{$('#settingsStatus').textContent='❌ Error: '+d.error;setTimeout(()=>$('#settingsStatus').textContent='',3000)}
  }catch(e){$('#settingsStatus').textContent='❌ Error: '+e.message;setTimeout(()=>$('#settingsStatus').textContent='',3000)}
}
</script>
</body>
</html>"""

# ---------------------------------------------------------------------------
# Flask Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/config")
def api_config():
    cfg = load_config()
    return jsonify({
        "provider": cfg.model.provider,
        "model": cfg.model.model_name,
        "has_key": bool(cfg.model.api_key),
        "providers": {k: v["label"] for k, v in PROVIDERS.items()},
    })


def _build_file_tree(path: Path, root: Path) -> list[dict]:
    items = []
    try:
        for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.name.startswith(".") or item.name == "__pycache__" or item.name == ".tmp":
                continue
            rel = str(item.relative_to(root))
            if item.is_dir():
                children = _build_file_tree(item, root)
                items.append({"name": item.name, "path": rel, "type": "dir", "children": children})
            else:
                items.append({"name": item.name, "path": rel, "type": "file"})
    except (PermissionError, OSError):
        pass
    return items


@app.route("/api/files")
def api_files():
    root = Path.cwd()
    return jsonify(_build_file_tree(root, root))


@app.route("/api/files/<path:filepath>")
def api_read_file(filepath: str):
    root = Path.cwd()
    full_path = (root / filepath).resolve()
    if not str(full_path).startswith(str(root.resolve())):
        return jsonify({"error": "Access denied"}), 403
    if not full_path.exists() or not full_path.is_file():
        return jsonify({"error": "File not found"}), 404
    try:
        content = full_path.read_text(encoding="utf-8", errors="replace")
        return Response(content, mimetype="text/plain; charset=utf-8")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    sid = session.get("sid", str(uuid.uuid4()))
    session["sid"] = sid

    if sid not in chat_histories:
        cfg = load_config()
        chat_histories[sid] = [{"role": "system", "content": build_system_prompt(cfg)}]

    chat_histories[sid].append({"role": "user", "content": user_msg})

    def generate():
        cfg = load_config()
        try:
            kwargs = get_litellm_kwargs(cfg)
            kwargs["messages"] = chat_histories[sid]
            kwargs["stream"] = True

            response = litellm.completion(**kwargs)
            full_content = ""

            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_content += delta
                    yield f"data: {json.dumps({'token': delta})}\n\n"

            chat_histories[sid].append({"role": "assistant", "content": full_content})

            blocks = extract_code_blocks(full_content)
            if blocks:
                yield f"data: {json.dumps({'status': 'Executing code...'})}\n\n"
                try:
                    final = process_llm_response(full_content, chat_histories[sid], cfg)
                    if final and final != full_content:
                        chat_histories[sid][-1]["content"] = final
                        yield f"data: {json.dumps({'status': 'Refining output...'})}\n\n"
                        for word in final.split(" "):
                            yield f"data: {json.dumps({'token': word + ' '})}\n\n"
                            time.sleep(0.008)
                except Exception as e:
                    yield f"data: {json.dumps({'status': 'Correction note: ' + str(e)})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            err_msg = str(e)
            if "auth" in err_msg.lower() or "key" in err_msg.lower() or "unauthorized" in err_msg.lower():
                hint = " Try `/connect` to update your API key."
            elif "model" in err_msg.lower() or "not found" in err_msg.lower():
                hint = " Try `/model <name>` to switch models."
            else:
                hint = ""
            yield f"data: {json.dumps({'error': err_msg + hint})}\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/model", methods=["POST"])
def api_switch_model():
    data = request.get_json()
    model_name = data.get("model", "").strip()
    if not model_name:
        return jsonify({"success": False, "error": "Model name required"}), 400
    try:
        cfg = load_config()
        cfg.model.model_name = model_name
        save_config(cfg)
        for sid in chat_histories:
            chat_histories[sid][0] = {"role": "system", "content": build_system_prompt(cfg)}
        return jsonify({"success": True, "model": model_name})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/connect", methods=["GET", "POST"])
def api_connect():
    if request.method == "GET":
        cfg = load_config()
        return jsonify({
            "provider": cfg.model.provider,
            "model": cfg.model.model_name,
            "api_base": cfg.model.api_base or "",
            "providers": {
                k: {
                    "label": v["label"],
                    "models": v["models"],
                    "default": v["default"],
                }
                for k, v in PROVIDERS.items()
            },
        })

    data = request.get_json()
    try:
        cfg = load_config()
        if "model" in data and data["model"]:
            cfg.model.model_name = data["model"]
        if "provider" in data and data["provider"]:
            cfg.model.provider = data["provider"]
        if "api_key" in data and data["api_key"]:
            cfg.model.api_key = data["api_key"]
            env_map = {
                "anthropic": "ANTHROPIC_API_KEY",
                "openai": "OPENAI_API_KEY",
                "google": "GEMINI_API_KEY",
                "groq": "GROQ_API_KEY",
                "openrouter": "OPENROUTER_API_KEY",
                "deepseek": "DEEPSEEK_API_KEY",
                "together": "TOGETHER_API_KEY",
                "mistral": "MISTRAL_API_KEY",
                "custom": "CUSTOM_API_KEY",
            }
            env_var = env_map.get(data.get("provider", cfg.model.provider), "")
            if env_var:
                os.environ[env_var] = data["api_key"]
        if "api_base" in data:
            cfg.model.api_base = data["api_base"] or None
        save_config(cfg)

        for sid in chat_histories:
            chat_histories[sid][0] = {"role": "system", "content": build_system_prompt(cfg)}

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def api_clear():
    sid = session.get("sid")
    if sid and sid in chat_histories:
        cfg = load_config()
        chat_histories[sid] = [{"role": "system", "content": build_system_prompt(cfg)}]
    return jsonify({"success": True})


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    console.print()
    console.print("[bold cyan]\u250F\u2501\u2501\u2501  2 M   C O D E   W e b   U I  \u2501\u2501\u2501\u2513[/bold cyan]")
    console.print("[bold cyan]\u2503[/bold cyan]  [green]Local:   http://localhost:5000[/green]  [bold cyan]\u2503[/bold cyan]")
    console.print("[bold cyan]\u2503[/bold cyan]  [dim]Press Ctrl+C to stop[/dim]        [bold cyan]\u2503[/bold cyan]")
    console.print("[bold cyan]\u2517\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B[/bold cyan]")
    console.print()
    app.run(debug=False, host="127.0.0.1", port=5000)
