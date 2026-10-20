<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Редактор жгута</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Geologica:wght@300;400;600;800&display=swap');
:root{--bg:#0d1117;--surface:#161b22;--surface2:#1c2128;--border:#30363d;--accent:#58a6ff;--green:#3fb950;--warn:#d29922;--danger:#f85149;--text:#e6edf3;--text2:#8b949e;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Geologica',sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column;overflow:hidden;}
.toolbar{background:var(--surface);border-bottom:1px solid var(--border);padding:10px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0;}
.logo{font-size:13px;font-weight:800;color:var(--accent);margin-right:8px;}
.btn{display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:6px;border:none;font-size:12px;font-family:'Geologica',sans-serif;font-weight:600;cursor:pointer;transition:all .15s;}
.btn-primary{background:var(--accent);color:#000;}
.btn-primary:hover{background:#79b8ff;}
.btn-success{background:var(--green);color:#000;}
.btn-success:hover{background:#56d364;}
.btn-outline{background:transparent;border:1px solid var(--border);color:var(--text);}
.btn-outline:hover{border-color:var(--accent);color:var(--accent);}
.btn-danger{background:transparent;border:1px solid var(--danger);color:var(--danger);}
.sep{width:1px;height:24px;background:var(--border);}
.hint{font-size:11px;color:var(--text2);margin-left:auto;}
.hint span{color:var(--accent);}
.main{display:flex;flex:1;overflow:hidden;}
.sidebar{width:290px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;}
.sidebar-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--text2);padding:12px 14px;border-bottom:1px solid var(--border);}
.sidebar-body{flex:1;overflow-y:auto;padding:10px;}
.conn-card{background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:10px;margin-bottom:8px;transition:border-color .15s;}
.conn-card.disabled{opacity:0.45;}
.conn-card.enabled{border-color:var(--green);}
.conn-header{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.conn-badge{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:var(--accent);flex:1;}
.toggle{position:relative;width:36px;height:20px;cursor:pointer;}
.toggle input{opacity:0;width:0;height:0;}
.toggle-slider{position:absolute;inset:0;background:var(--border);border-radius:20px;transition:.2s;}
.toggle input:checked+.toggle-slider{background:var(--green);}
.toggle-slider:before{content:'';position:absolute;width:14px;height:14px;left:3px;top:3px;background:#fff;border-radius:50%;transition:.2s;}
.toggle input:checked+.toggle-slider:before{transform:translateX(16px);}
.conn-remove{background:none;border:none;color:var(--danger);cursor:pointer;font-size:14px;padding:0;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:6px;}
label{font-size:11px;color:var(--text2);display:block;margin-bottom:2px;}
input,select{width:100%;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:4px;padding:5px 8px;font-size:12px;font-family:'Geologica',sans-serif;outline:none;}
input:focus,select:focus{border-color:var(--accent);}
select option{background:var(--bg);}
.canvas-wrap{flex:1;position:relative;overflow:hidden;background:var(--bg);background-image:radial-gradient(circle,#30363d 1px,transparent 1px);background-size:32px 32px;}
svg.canvas{position:absolute;inset:0;width:100%;height:100%;}
.node{cursor:grab;user-select:none;}
.node:active{cursor:grabbing;}
.node-rect{fill:#161b22;stroke:#30363d;stroke-width:1.5;}
.node.active-node .node-rect{stroke:#3fb950;}
.node-title{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;fill:#58a6ff;}
.node-sub{font-size:10px;fill:#8b949e;font-family:'Geologica',sans-serif;}
.node-mark{font-size:11px;fill:#d29922;font-family:'JetBrains Mono',monospace;}
.node-disabled .node-rect{stroke:#30363d;fill:#0d1117;}
.node-disabled .node-title{fill:#30363d;}
.node-disabled .node-sub{fill:#30363d;}
.gear{cursor:pointer;fill:#58a6ff;font-size:12px;}
.gear:hover{fill:#79b8ff;}
.port{cursor:crosshair;fill:#30363d;stroke:#58a6ff;stroke-width:1.5;}
.port:hover,.port.active{fill:#58a6ff;}
.edge{stroke:#30363d;stroke-width:2;fill:none;cursor:pointer;transition:stroke .15s;}
.edge:hover,.edge.selected{stroke:#58a6ff;}
.edge-label{font-size:10px;fill:#8b949e;font-family:'JetBrains Mono',monospace;pointer-events:none;}
.temp-line{stroke:#58a6ff;stroke-width:1.5;stroke-dasharray:6 4;fill:none;pointer-events:none;}
.panel{position:absolute;right:16px;top:16px;width:270px;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:10;}
.panel-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--text2);margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;}
.panel-close{background:none;border:none;color:var(--text2);cursor:pointer;font-size:16px;padding:0;}
.panel-close:hover{color:var(--danger);}
.field{margin-bottom:10px;}
.check-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.check-row input[type=checkbox]{width:auto;}
.check-row label{font-size:12px;color:var(--text);margin:0;}
select optgroup{color:var(--text2);font-size:11px;background:var(--surface2);}
.node-label-rect{fill:#1c2128;stroke:#d29922;stroke-width:1.5;}
.node-label-title{font-size:11px;font-weight:700;fill:#d29922;font-family:'JetBrains Mono',monospace;}
</style>
</head>
<body>

<div class="toolbar">
  <span class="logo">⚡ ЖГУТ</span>
  <div class="sep"></div>
  <button class="btn btn-outline" onclick="addNode()">+ Разъём</button>
  <button class="btn btn-outline" onclick="addLabel()">+ Бирка</button>
  <button class="btn btn-outline" onclick="clearAll()">🗑 Очистить</button>
  <div class="sep"></div>
  <button class="btn btn-success" onclick="calcSpec()">⚡ Рассчитать</button>
  <div class="sep"></div>
  <span class="hint">Включи разъёмы → тяни от <span>●</span> для соединения → кликни линию / ⚙ / бирку</span>
</div>

<div class="main">
  <div class="sidebar">
    <div class="sidebar-title">Разъёмы (включи нужные)</div>
    <div class="sidebar-body" id="sidebarBody"></div>
  </div>

  <div class="canvas-wrap" id="canvasWrap">
    <svg class="canvas" id="canvas" onmousemove="onMouseMove(event)" onmouseup="onMouseUp(event)">
      <g id="edgesGroup"></g>
      <g id="nodesGroup"></g>
      <path id="tempLine" class="temp-line" style="display:none"/>
    </svg>

    <!-- Панель связи -->
    <div id="edgePanel" class="panel" style="display:none">
      <div class="panel-title">Свойства связи <button class="panel-close" onclick="closePanels()">✕</button></div>
      <div class="field"><label>Длина участка, м</label><input type="number" id="epLength" value="1.8" step="0.1" min="0.1" onchange="updateEdge()"></div>
      <div class="field"><label>Марка провода</label>
        <select id="epWire" onchange="updateEdge()"></select>
      </div>
      <div class="check-row"><input type="checkbox" id="epShield" onchange="updateEdge()"><label for="epShield">Экран (ПЛМ)</label></div>
      <div class="check-row"><input type="checkbox" id="epPet" onchange="updateEdge()"><label for="epPet">Оплётка (PET)</label></div>
      <button class="btn btn-danger" style="width:100%;margin-top:4px" onclick="deleteEdge()">Удалить связь</button>
    </div>

    <!-- Панель разъёма -->
    <div id="nodePanel" class="panel" style="display:none">
      <div class="panel-title">Разъём <button class="panel-close" onclick="closePanels()">✕</button></div>
      <div id="nodePanelBody"></div>
    </div>

    <!-- Панель бирки -->
    <div id="labelPanel" class="panel" style="display:none">
      <div class="panel-title">Бирка <button class="panel-close" onclick="closePanels()">✕</button></div>
      <div class="check-row"><input type="checkbox" id="lbMark" onchange="updateLabel()"><label for="lbMark">ТТ маркировочная</label></div>
      <div class="field"><select id="lbMarkSize" onchange="updateLabel()"></select></div>
      <div class="check-row"><input type="checkbox" id="lbGlue" onchange="updateLabel()"><label for="lbGlue">ТТ с клеем</label></div>
      <div class="field"><select id="lbGlueSize" onchange="updateLabel()"></select></div>
      <div class="check-row"><input type="checkbox" id="lbSticker" onchange="updateLabel()"><label for="lbSticker">Этикетка TZe-221</label></div>
      <div class="field"><label>Подпись бирки</label><input id="lbText" onchange="updateLabel()" placeholder='напр. "А1"'></div>
      <button class="btn btn-danger" style="width:100%;margin-top:4px" onclick="deleteLabel()">Удалить бирку</button>
    </div>
  </div>
</div>

<script>
// ===== ТАБЛИЦА ДИАМЕТРОВ ПРОВОДОВ (мм) =====
const WIRE_D={
  "МГТФ 0,03":0.56,"МГТФ 0,05":0.62,"МГТФ 0,07":0.72,
  "МГТФ 0,08(1x0.07)":0.75,"МГТФ 0,08(1x0.10)":0.85,"МГТФ 0,08(1х0.12)":0.87,
  "МГТФ 0,12(1х0.2)":1.04,"МГТФ 0,12":0.82,"МГТФ 0,14(1x0.14)":0.90,
  "МГТФ 0,15(1х0.35)":1.19,"МГТФ 0,20":1.00,"МГТФ 0,35":1.20,
  "МГТФ 0,50":1.40,"МГТФ 0,75":1.60,"МГТФ 1":1.65,
  "МГТФ 2x0.07":1.7,"МГТФ 2x0.12":2.0,
  "МГТФЭ 0,07":1.3,"МГТФЭ 0.08(1х12)":1.6,"МГТФЭ 0.08(2х07)":1.7,
  "МГТФЭ 0.08(2х12)":2.5,"МГТФЭ 0.08(3х12)":3.0,
  "МГТФЭ 2x0.20":2.7,"МГТФЭ 2x0.35":3.0,
  "МГТФЭ 2x0.5":3.5,"МГТФЭ 4x0.5":4.5,
  "МГШВ 0.14":1.4,"МГШВ 0.2":1.6,"МГШВ 0.35":1.9,
  "МГШВ 0.5":2.2,"МГШВ 0.75":2.5,"МГШВ 1":2.8,"МГШВ 1.5":3.0,
  "МГШВЭ 0.14":2.0,"МГШВЭ 0.2":2.2,"МГШВЭ 0.35":2.5,
  "МГШВЭ 0.5":2.8,"МГШВЭ 0.75":3.3,
  "НВ-3 0.75":2.1,"НВ-3 1.5":2.5,
  "НВ-600(бел.) 0.35":1.38,"НВ-600 0.08":1.2,"НВ-600 0.12":1.30,
  "НВ-600 0.2":1.5,"НВ-600 0.35":1.6,"НВ-600 0.5":1.8,
  "НВ-600 0.75":2.1,"НВ-600 1":2.2,"НВ-600 1.5":2.5,"НВ-600 2.5":3.2,
  "НВ-1000 0.08":1.4,"НВ-1000 0.12":1.50,"НВ-1000 0.2":1.7,
  "НВ-1000 0.35":1.8,"НВ-1000 0.5":2.0,"НВ-1000 0.75":2.3,
  "НВ-1000 1":2.4,"НВ-1000 1.5":2.7,"НВ-1000 2.5":3.3,
  "ПВМП-2 0.12":1.60,"ПВМП-2.5 0.35":2.10,
  "ПВС 3х2.5":11.4,"ПЩ 0.5":1.05,
  "Ethernet_кат.5е U/UTP_24AWG":5.3,"Ethernet_кат.5е F/UTP_24AWG_PVC":5.3,
  "Ethernet_кат.5е SF/UTP_26/7AWG_PVC":5.6
};

// Кабель = только Ethernet
function isCable(w){return w.startsWith("Ethernet");}

// ===== ТАБЛИЦА ПЛМ (ПЛЕТЁНКА) =====
const PLM_TABLE = [
  ["ПМЛ 2х4",  {2:1, 3:1.225}],
  ["ПМЛ 4х5",  {4:1}],
  ["ПМЛ 3х6",  {5:1.350}],
  ["ПМЛ 6х10", {6:1, 7:1.150, 8:1.300, 9:1.450}],
  ["ПМЛ 10х16",{10:1, 11:1.100, 12:1.200, 13:1.225, 14:1.400, 15:1.500}],
  ["ПМЛ 16х24",{16:1, 17:1.075, 18:1.15, 19:1.225, 20:1.3, 21:1.375, 22:1.45, 23:1.525}],
  ["ПМЛ 24х30",{24:1, 25:1.05, 26:1.1, 27:1.15, 28:1.2, 29:1.25, 30:1.3}],
  ["ПМЛ 30х40",{30:1, 31:1.04, 32:1.08, 33:1.12, 34:1.6, 35:1.2, 36:1.24, 37:1.28}]
];

// ===== ТАБЛИЦА PET =====
const PET_TABLE=[
  ["PET-3",  [[2,1.0],[3,1.1]]],
  ["PET-6",  [[4,1.0],[5,1.05],[6,1.1]]],
  ["PET-10", [[7,1.0],[8,1.05],[9,1.1]]],
  ["PET-15", [[10,1.0],[12,1.1],[14,1.15],[16,1.2],[18,1.2]]],
  ["PET-20", [[19,1.15],[20,1.2]]],
  ["PET-25", [[22,1.0],[26,1.2],[30,1.25],[32,1.5],[33,1.6],[40,2.5]]],
  ["PET-ES-35", [[32,1.2],[33,1.25],[40,1.5],[44,1.73],[45,1.89],[50,2.96]]],
  ["PET-ES-50", [[44,1.42],[45,1.48],[50,1.75],[55,2.36]]]
];
const GLUE_T=[[3.1,1.0,0.95],[4.6,1.8,1.1],[6.4,2.4,1.2],[7.7,2.9,1.3],[9.4,3.4,1.4],[12.5,4.4,1.5],[14.8,5.4,1.8],[18.8,6.5,2.0],[25.0,8.8,2.1],[30.0,10.5,2.1]];
const MARK_T=[[2.4,0.8,0.53],[6.4,2.0,0.63],[9.0,3.0,0.63],[12.7,4.0,0.68],[19.1,6.0,0.9],[25.4,8.0,1.0],[38.1,12.7,1.1]];
const GOST1=[[300,15,10],[500,20,15],[2000,35,25],[5000,50,35],[10000,100,65],[15000,150,100],[20000,200,150],[25000,250,170],[30000,300,200]];
const T72=[[12,30],[17,40],[25,50],[99999,60]];

// ===== СОСТОЯНИЕ =====
let nodes=[], edges=[], selEdge=null, selNode=null, selLabel=null;
let dragging=null, dragOff={x:0,y:0};
let connecting=null;
let idSeq=1;
const NW=160, NH=80;      // разъём
const LW=100, LH=42;      // бирка

function addNode(d={}){
  const id=idSeq++;
  const i=nodes.length;
  const cols=3;
  nodes.push({
    kind:'connector', id,
    name:d.name||`Х${id}`, type:d.type||'', contacts:d.contacts||34, marking:d.marking||'',
    enabled:false, x:60+(i%cols)*200, y:60+Math.floor(i/cols)*140,
    // флаги панели
    fContactsTT:true, fThreads:true, fTape69:true, fTape130:false
  });
  renderAll();
}

function addLabel(d={}){
  const id=idSeq++;
  const n=nodes.length;
  nodes.push({
    kind:'label', id,
    name:d.name||`Б${id}`, enabled:true,
    x:60+(n%4)*180, y:60+Math.floor(n/4)*120,
    lbMark:true, lbGlue:true, lbSticker:false,
    markSize:0, glueSize:0,
    text:d.text||''
  });
  renderAll();
}

function removeNode(id){
  nodes=nodes.filter(n=>n.id!==id);
  edges=edges.filter(e=>e.from!==id&&e.to!==id);
  renderAll();
}

function toggleNode(id){
  const n=nodes.find(n=>n.id===id);
  if(n){
    n.enabled=!n.enabled;
    if(!n.enabled) edges=edges.filter(e=>e.from!==id&&e.to!==id);
  }
  renderAll();
}

function updateNode(id,field,val){
  const n=nodes.find(n=>n.id===id);
  if(n) n[field]=field==='contacts'?+val:val;
  renderAll();
}
function updateNodeFlag(id,field,val){
  const n=nodes.find(n=>n.id===id); if(n) n[field]=val; renderAll();
}

function renderAll(){renderSidebar();renderEdges();renderNodes();}

function renderSidebar(){
  const sb=document.getElementById('sidebarBody');
  sb.innerHTML='';
  nodes.filter(n=>n.kind==='connector').forEach((n,i)=>{
    const d=document.createElement('div');
    d.className=`conn-card ${n.enabled?'enabled':'disabled'}`;
    d.innerHTML=`
      <div class="conn-header">
        <span class="conn-badge">${n.name||`Х${i+1}`}</span>
        <label class="toggle"><input type="checkbox" ${n.enabled?'checked':''} onchange="toggleNode(${n.id})"><span class="toggle-slider"></span></label>
        <button class="conn-remove" onclick="removeNode(${n.id})">✕</button>
      </div>
      ${n.enabled?`
      <div class="form-row">
        <div><label>Обозначение</label><input value="${n.name}" onchange="updateNode(${n.id},'name',this.value)"></div>
        <div><label>Контактов</label><input type="number" value="${n.contacts}" min="1" onchange="updateNode(${n.id},'contacts',this.value)"></div>
      </div>
      <div class="form-row">
        <div><label>Маркировка</label><input value="${n.marking}" placeholder='"A"' onchange="updateNode(${n.id},'marking',this.value)"></div>
        <div><label>Тип разъёма</label><input value="${n.type}" placeholder="DB-37F..." onchange="updateNode(${n.id},'type',this.value)"></div>
      </div>`:'<div style="font-size:11px;color:var(--text2);padding:2px 0">Выключен — включи тумблер</div>'}
    `;
    sb.appendChild(d);
  });
  // Бирки
  const labels=nodes.filter(n=>n.kind==='label');
  if(labels.length){
    const h=document.createElement('div');
    h.style.cssText='font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text2);padding:12px 4px 4px';
    h.textContent='Бирки';
    sb.appendChild(h);
    labels.forEach(l=>{
      const d=document.createElement('div');
      d.className='conn-card enabled';
      d.innerHTML=`
        <div class="conn-header">
          <span class="conn-badge" style="color:var(--warn)">${l.name}</span>
          <button class="conn-remove" onclick="removeNode(${l.id})">✕</button>
        </div>
        <div style="font-size:11px;color:var(--text2)">
          ${l.lbMark?'ТТ марк. ':''}${l.lbGlue?'ТТ клей ':''}${l.lbSticker?'Этикетка':''}
          ${!l.lbMark&&!l.lbGlue&&!l.lbSticker?'<i style="color:var(--warn)">точка расхождения</i>':''}
        </div>`;
      sb.appendChild(d);
    });
  }
}

function renderNodes(){
  const g=document.getElementById('nodesGroup');
  g.innerHTML='';
  nodes.forEach(n=>{
    if(n.kind==='connector') renderConnector(g,n);
    else renderLabel(g,n);
  });
}

function renderConnector(g,n){
  const el=document.createElementNS('http://www.w3.org/2000/svg','g');
  el.setAttribute('class',`node ${n.enabled?'active-node':'node-disabled'}`);
  el.setAttribute('transform',`translate(${n.x},${n.y})`);

  const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
  rect.setAttribute('class','node-rect');
  rect.setAttribute('width',NW);rect.setAttribute('height',NH);rect.setAttribute('rx',8);
  el.appendChild(rect);

  const title=document.createElementNS('http://www.w3.org/2000/svg','text');
  title.setAttribute('class','node-title');
  title.setAttribute('x',NW/2);title.setAttribute('y',24);title.setAttribute('text-anchor','middle');
  title.textContent=n.name||'Х?';
  el.appendChild(title);

  const sub=document.createElementNS('http://www.w3.org/2000/svg','text');
  sub.setAttribute('class','node-sub');
  sub.setAttribute('x',NW/2);sub.setAttribute('y',42);sub.setAttribute('text-anchor','middle');
  sub.textContent=`${n.contacts} конт.`;
  el.appendChild(sub);

  if(n.marking){
    const mk=document.createElementNS('http://www.w3.org/2000/svg','text');
    mk.setAttribute('class','node-mark');
    mk.setAttribute('x',NW/2);mk.setAttribute('y',60);mk.setAttribute('text-anchor','middle');
    mk.textContent=n.marking;
    el.appendChild(mk);
  }

  // Шестерёнка (панель)
  if(n.enabled){
    const gear=document.createElementNS('http://www.w3.org/2000/svg','text');
    gear.setAttribute('class','gear');
    gear.setAttribute('x',NW-14);gear.setAttribute('y',16);
    gear.setAttribute('text-anchor','middle');
    gear.textContent='⚙';
    gear.addEventListener('mousedown',e=>{e.stopPropagation();openNodePanel(n.id);});
    el.appendChild(gear);
  }

  if(n.enabled){
    const port=document.createElementNS('http://www.w3.org/2000/svg','circle');
    port.setAttribute('class','port');
    port.setAttribute('cx',NW);port.setAttribute('cy',NH/2);port.setAttribute('r',5);
    port.addEventListener('mousedown',e=>{e.stopPropagation();startConnect(e,n,'R');});
    el.appendChild(port);
  }

  if(n.enabled){
    el.addEventListener('mousedown',e=>{
      if(e.target.classList.contains('port')||e.target.classList.contains('gear'))return;
      dragging={id:n.id};
      const pt=svgPoint(e);
      dragOff={x:pt.x-n.x,y:pt.y-n.y};
      e.preventDefault();
    });
  }
  g.appendChild(el);
}

function renderLabel(g,n){
  const el=document.createElementNS('http://www.w3.org/2000/svg','g');
  el.setAttribute('class','node');
  el.setAttribute('transform',`translate(${n.x},${n.y})`);

  const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
  rect.setAttribute('class','node-label-rect');
  rect.setAttribute('width',LW);rect.setAttribute('height',LH);rect.setAttribute('rx',6);
  el.appendChild(rect);

  const title=document.createElementNS('http://www.w3.org/2000/svg','text');
  title.setAttribute('class','node-label-title');
  title.setAttribute('x',LW/2);title.setAttribute('y',16);title.setAttribute('text-anchor','middle');
  title.textContent=n.name;
  el.appendChild(title);

  const sub=document.createElementNS('http://www.w3.org/2000/svg','text');
  sub.setAttribute('class','node-sub');
  sub.setAttribute('x',LW/2);sub.setAttribute('y',32);sub.setAttribute('text-anchor','middle');
  sub.textContent=n.text||'';
  el.appendChild(sub);

  // Две точки: слева и справа
  const pL=document.createElementNS('http://www.w3.org/2000/svg','circle');
  pL.setAttribute('class','port');
  pL.setAttribute('cx',0);pL.setAttribute('cy',LH/2);pL.setAttribute('r',5);
  pL.addEventListener('mousedown',e=>{e.stopPropagation();startConnect(e,n,'L');});
  el.appendChild(pL);

  const pR=document.createElementNS('http://www.w3.org/2000/svg','circle');
  pR.setAttribute('class','port');
  pR.setAttribute('cx',LW);pR.setAttribute('cy',LH/2);pR.setAttribute('r',5);
  pR.addEventListener('mousedown',e=>{e.stopPropagation();startConnect(e,n,'R');});
  el.appendChild(pR);

  el.addEventListener('mousedown',e=>{
    if(e.target.classList.contains('port'))return;
    dragging={id:n.id};
    const pt=svgPoint(e);
    dragOff={x:pt.x-n.x,y:pt.y-n.y};
    e.preventDefault();
  });
  el.addEventListener('click',e=>{
    if(e.target.classList.contains('port'))return;
    openLabelPanel(n.id);
  });

  g.appendChild(el);
}

function portPos(n,side){
  if(n.kind==='connector') return {x:n.x+NW, y:n.y+NH/2};
  if(side==='L') return {x:n.x,       y:n.y+LH/2};
  return            {x:n.x+LW,  y:n.y+LH/2};
}

function renderEdges(){
  const g=document.getElementById('edgesGroup');
  g.innerHTML='';
  edges.forEach(e=>{
    const from=nodes.find(n=>n.id===e.from);
    const to=nodes.find(n=>n.id===e.to);
    if(!from||!to)return;
    const p1=portPos(from,e.fromSide), p2=portPos(to,e.toSide);
    const cx=(p1.x+p2.x)/2;
    const path=document.createElementNS('http://www.w3.org/2000/svg','path');
    path.setAttribute('class',`edge${selEdge===e.id?' selected':''}`);
    path.setAttribute('d',`M${p1.x},${p1.y} C${cx},${p1.y} ${cx},${p2.y} ${p2.x},${p2.y}`);
    path.addEventListener('click',ev=>{ev.stopPropagation();openEdgePanel(e.id);});
    g.appendChild(path);
    const lx=(p1.x+p2.x)/2,ly=Math.min(p1.y,p2.y)-10;
    const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
    txt.setAttribute('class','edge-label');
    txt.setAttribute('x',lx);txt.setAttribute('y',ly);txt.setAttribute('text-anchor','middle');
    let tag=`${e.length}м · ${e.wire}`;
    if(e.shield) tag+=' · ПЛМ';
    if(e.pet)    tag+=' · PET';
    txt.textContent=tag;
    g.appendChild(txt);
  });
}

function startConnect(e,node,side){
  const pt=svgPoint(e);
  const pos=portPos(node,side);
  connecting={nodeId:node.id,side,x:pos.x,y:pos.y};
  const tl=document.getElementById('tempLine');
  tl.style.display='block';
  tl.setAttribute('d',`M${pos.x},${pos.y} L${pt.x},${pt.y}`);
}

function onMouseMove(e){
  const pt=svgPoint(e);
  if(connecting){
    document.getElementById('tempLine').setAttribute('d',`M${connecting.x},${connecting.y} L${pt.x},${pt.y}`);
  }
  if(dragging){
    const n=nodes.find(n=>n.id===dragging.id);
    if(n){n.x=pt.x-dragOff.x;n.y=pt.y-dragOff.y;}
    renderEdges();renderNodes();
  }
}

function onMouseUp(e){
  if(connecting){
    const pt=svgPoint(e);
    // ищем цель
    let target=null,targetSide=null;
    for(const n of nodes){
      if(n.id===connecting.nodeId) continue;
      if(n.kind==='connector'){
        if(n.enabled&&pt.x>=n.x&&pt.x<=n.x+NW&&pt.y>=n.y&&pt.y<=n.y+NH){
          target=n;targetSide='R';break;
        }
      } else {
        // бирка: две точки
        const dL=Math.hypot(pt.x-n.x,pt.y-(n.y+LH/2));
        const dR=Math.hypot(pt.x-(n.x+LW),pt.y-(n.y+LH/2));
        const dIn=Math.hypot(pt.x-(n.x+LW/2),pt.y-(n.y+LH/2));
        if(dL<20||dR<20||dIn<50){target=n;targetSide=(dL<dR?'L':'R');break;}
      }
    }
    if(target){
      const exists=edges.find(ed=>(ed.from===connecting.nodeId&&ed.to===target.id)||(ed.from===target.id&&ed.to===connecting.nodeId));
      if(!exists){
        edges.push({
          id:idSeq++,
          from:connecting.nodeId, fromSide:connecting.side,
          to:target.id, toSide:targetSide,
          length:1.8, wire:'МГТФ 0,07', shield:false, pet:true
        });
      }
      renderEdges();
    }
    document.getElementById('tempLine').style.display='none';
    connecting=null;
  }
  dragging=null;
}

// ===== ПАНЕЛИ =====
function closePanels(){
  selEdge=null;selNode=null;selLabel=null;
  document.getElementById('edgePanel').style.display='none';
  document.getElementById('nodePanel').style.display='none';
  document.getElementById('labelPanel').style.display='none';
  renderEdges();
}

function openEdgePanel(id){
  closePanels();
  selEdge=id;
  const e=edges.find(x=>x.id===id); if(!e)return;
  document.getElementById('epLength').value=e.length;
  document.getElementById('epWire').value=e.wire;
  document.getElementById('epShield').checked=!!e.shield;
  document.getElementById('epPet').checked=!!e.pet;
  document.getElementById('edgePanel').style.display='block';
  renderEdges();
}
function updateEdge(){
  const e=edges.find(x=>x.id===selEdge);if(!e)return;
  e.length=+document.getElementById('epLength').value;
  e.wire=document.getElementById('epWire').value;
  e.shield=document.getElementById('epShield').checked;
  e.pet=document.getElementById('epPet').checked;
  renderEdges();
}
function deleteEdge(){edges=edges.filter(e=>e.id!==selEdge);closePanels();renderEdges();}

function openNodePanel(id){
  closePanels(); selNode=id;
  const n=nodes.find(x=>x.id===id); if(!n)return;
  const b=document.getElementById('nodePanelBody');
  b.innerHTML=`
    <div class="check-row"><input type="checkbox" ${n.fContactsTT?'checked':''} onchange="updateNodeFlag(${n.id},'fContactsTT',this.checked)"><label>ТТ на контакты</label></div>
    <div class="check-row"><input type="checkbox" ${n.fThreads?'checked':''} onchange="updateNodeFlag(${n.id},'fThreads',this.checked)"><label>Нитки</label></div>
    <div class="check-row"><input type="checkbox" ${n.fTape69?'checked':''} onchange="updateNodeFlag(${n.id},'fTape69',this.checked)"><label>Лента 3М Scotch 69</label></div>
    <div class="check-row"><input type="checkbox" ${n.fTape130?'checked':''} onchange="updateNodeFlag(${n.id},'fTape130',this.checked)"><label>Лента 3М Scotch 130С</label></div>
  `;
  document.getElementById('nodePanel').style.display='block';
}

function openLabelPanel(id){
  closePanels(); selLabel=id;
  const n=nodes.find(x=>x.id===id); if(!n)return;
  // селекты размеров
  const sm=document.getElementById('lbMarkSize');
  sm.innerHTML='';
  MARK_T.forEach((t,i)=>{const o=document.createElement('option');o.value=i;o.textContent=`${t[0]}/${t[1]}`;sm.appendChild(o);});
  const sg=document.getElementById('lbGlueSize');
  sg.innerHTML='';
  GLUE_T.forEach((t,i)=>{const o=document.createElement('option');o.value=i;o.textContent=`${t[0]}/${t[1]}`;sg.appendChild(o);});
  document.getElementById('lbMark').checked=n.lbMark;
  document.getElementById('lbGlue').checked=n.lbGlue;
  document.getElementById('lbSticker').checked=n.lbSticker;
  document.getElementById('lbText').value=n.text||'';
  sm.value=n.markSize||0;
  sg.value=n.glueSize||0;
  document.getElementById('labelPanel').style.display='block';
}
function updateLabel(){
  const n=nodes.find(x=>x.id===selLabel); if(!n)return;
  n.lbMark=document.getElementById('lbMark').checked;
  n.lbGlue=document.getElementById('lbGlue').checked;
  n.lbSticker=document.getElementById('lbSticker').checked;
  n.markSize=+document.getElementById('lbMarkSize').value;
  n.glueSize=+document.getElementById('lbGlueSize').value;
  n.text=document.getElementById('lbText').value;
  renderSidebar();
}
function deleteLabel(){nodes=nodes.filter(n=>n.id!==selLabel);edges=edges.filter(e=>e.from!==selLabel&&e.to!==selLabel);closePanels();renderAll();}

function svgPoint(e){
  const svg=document.getElementById('canvas');
  const pt=svg.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;
  return pt.matrixTransform(svg.getScreenCTM().inverse());
}

function clearAll(){if(confirm('Очистить всё?')){nodes=[];edges=[];idSeq=1;renderAll();closePanels();}}

// ===== РАСЧЁТ =====
function gostTol(mm){for(const[l,p,m]of GOST1)if(mm<=l)return Math.min(p,m);return 200;}
function calcLen(m){const mm=m*1000;return Math.ceil((mm+gostTol(mm))*1.1)/1000;}
function calcD(n,dw){return +(1.3*Math.sqrt(n)*dw).toFixed(2);}
function ru1(v){return Math.ceil(v*10)/10;}

function selPET(d){
  for(const[nm,e]of PET_TABLE){
    const ds=e.map(x=>x[0]);
    if(Math.min(...ds)<=d&&d<=Math.max(...ds)){
      for(const[pd,c]of[...e].sort((a,b)=>a[0]-b[0]))if(pd>=d)return[nm,c];
    }
  }
  return['Не определён',null];
}
function selPLM(D){
  const d=Math.ceil(D); // вверх до целого
  if(d<2||d>37) return null;
  for(const[nm,map]of PLM_TABLE){
    if(map[d]!==undefined) return [nm,map[d]];
  }
  return null;
}
function selGlueIdx(d){
  for(let i=0;i<GLUE_T.length;i++){const t=GLUE_T[i];if(t[0]-t[2]*2>=d)return i;}
  return GLUE_T.length-1;
}
function selMarkIdx(d){
  for(let i=0;i<MARK_T.length;i++){const t=MARK_T[i];if(t[0]-t[2]*2>=d)return i;}
  return MARK_T.length-1;
}
function t72(d){for(const[dm,l]of T72)if(d<=dm)return l;return 60;}
function fmtGlue(t,L){return `Трубка термоусаживаемая с клеевым слоем TCT GW1 3Х Raychman ${t[0]}/${t[1]} L=(${L}±${L===5?1:2}) мм черная`;}
function fmtMark(t,L){return `ТМАРК-НГ-3П ТУ 22.21.29-005-65321637-2019 ${t[0]}/${t[1]} мм L=(${L}±2) мм белая`;}
function fmtPLM(name){return `Плетёнка ${name} ТУ 4833-002-08558606-95`;}

function calcSpec(){
  const activeNodes=nodes.filter(n=>n.kind==='connector'&&n.enabled);
  const activeLabels=nodes.filter(n=>n.kind==='label');
  if(activeNodes.length<2){alert('Включи минимум 2 разъёма');return;}
  if(edges.length<1){alert('Соедини разъёмы линиями');return;}

  // Главный = с наибольшим числом контактов
  const main=[...activeNodes].sort((a,b)=>b.contacts-a.contacts)[0];

  // Считаем "ветки": от главного к каждому другому разъёму (через граф, если есть бирки — просто по edges)
  // PET/ПЛМ на ветку считаем по диаметру СУММЫ проводов на пути от main к периферийному разъёму.
  // Для простоты — как раньше: каждая связь — это ветка (бирки не ломают расчёт).
  // Но для PET и ПЛМ нужно суммировать провода на ветке. Реализуем через "проход" по графу.

  // Строим граф
  const adj={};
  nodes.forEach(n=>adj[n.id]=[]);
  edges.forEach(e=>{
    adj[e.from].push({to:e.to,e,side:e.fromSide});
    adj[e.to].push({to:e.from,e,side:e.toSide});
  });

  // Для каждой ветки (main → периферийный разъём) — собираем список рёбер
  function pathEdges(startId,endId){
    const prev={};
    const q=[startId]; prev[startId]=null;
    while(q.length){
      const cur=q.shift();
      if(cur===endId) break;
      for(const v of adj[cur]){
        if(prev[v.to]===undefined){
          prev[v.to]={from:cur,e:v.e};
          q.push(v.to);
        }
      }
    }
    if(prev[endId]===undefined) return null;
    const list=[];let cur=endId;
    while(prev[cur]){list.push(prev[cur].e);cur=prev[cur].from;}
    return list.reverse();
  }

  // Определяем ветки: для каждого периферийного разъёма (не main) путь от main
  const branches=[]; // {node, edges:[...], wire, contacts, L, shield, pet}
  activeNodes.forEach(target=>{
    if(target.id===main.id)return;
    const list=pathEdges(main.id,target.id);
    if(!list)return;
    // Определяем "основной" провод ветки — по последнему ребру
    const lastE=list[list.length-1];
    // экран и PET: если ХОТЯ БЫ на одном ребре ветки включено — применяем (по твоему правилу "как будто бирки нет")
    const shield=list.some(e=>e.shield);
    const pet   =list.some(e=>e.pet);
    // длина ветки = сумма длин
    const totalM=list.reduce((s,e)=>s+e.length,0);
    const Lc=calcLen(totalM);
    branches.push({target, edges:list, wire:lastE.wire, contacts:target.contacts, L:Lc, shield, pet});
  });

  const spec=[];
  let n=1;
  // вспомогательные словари
  const cables={}; // кабель
  const wires={};  // провод
  const petMap={};
  const plmMap={};
  const glueMap={};
  const markMap={};

  // Провод/кабель по веткам
  branches.forEach(b=>{
    const total=b.contacts*b.L;
    const dst=isCable(b.wire)?cables:wires;
    dst[b.wire]=(dst[b.wire]||0)+total;
  });

  // PET и ПЛМ по диаметру ветки
  branches.forEach(b=>{
    const dw=WIRE_D[b.wire]||0.72;
    const Db=calcD(b.contacts,dw);
    const Dp=+(Db+(b.shield?0.5:0)+(b.pet?0.5:0)).toFixed(2);

    if(b.pet){
      const[pn,pc]=selPET(Dp);
      if(pc) petMap[pn]=(petMap[pn]||0)+ru1(b.L*pc);
    }
    if(b.shield){
      const plm=selPLM(Dp);
      if(plm){
        const[nm,k]=plm;
        plmMap[nm]=(plmMap[nm]||0)+ru1(b.L*k);
      }
    }
  });

  // ТТ с клеем и ТТ маркировка у КАЖДОЙ ВЕТКИ (на конечный разъём)
  // + у бирок — из панели
  // ТТ у разъёмов
  activeNodes.forEach(nd=>{
    // ищем ветку, где nd — целевой
    const b=branches.find(x=>x.target.id===nd.id) || branches.find(x=>x.target.id===main.id);
    const wire = b?b.wire:'МГТФ 0,07';
    const cont = nd.contacts;
    const dw=WIRE_D[wire]||0.72;
    const Dc=calcD(cont,dw);
    const Dcp=+(Dc+0.5).toFixed(2);
    // ТТ с клеем
    const gi=selGlueIdx(Dcp);
    const gt=GLUE_T[gi];
    const gl=t72(Dcp);
    const key=fmtGlue(gt,gl);
    glueMap[key]=(glueMap[key]||0)+1;
    // ТТ маркировка у разъёмов с маркировкой
    if(nd.marking){
      const mi=selMarkIdx(Dcp);
      const mk=MARK_T[mi];
      const key2=fmtMark(mk,10);
      markMap[key2]=(markMap[key2]||0)+1;
    }
  });

  // Бирки
  const lbMarkMap={};
  const lbGlueMap={};
  const lbStickerMap={};
  activeLabels.forEach(l=>{
    if(l.lbMark){const t=MARK_T[l.markSize]||MARK_T[0];const key=fmtMark(t,10);lbMarkMap[key]=(lbMarkMap[key]||0)+1;}
    if(l.lbGlue){const t=GLUE_T[l.glueSize]||GLUE_T[0];const key=fmtGlue(t,t72(t[0]));lbGlueMap[key]=(lbGlueMap[key]||0)+1;}
    if(l.lbSticker){const key='ФТКС.754463.060 Этикетка самоклеящаяся TZe-221 9х60 Brother';lbStickerMap[key]=(lbStickerMap[key]||0)+1;}
  });

  // ТТ на контакты (RBF) — по разъёмам с флагом
  let ttContacts=0;
  activeNodes.forEach(nd=>{ if(nd.fContactsTT) ttContacts+=nd.contacts; });

  // Нитки — по разъёмам с флагом
  let threadsM=0;
  activeNodes.forEach(nd=>{ if(nd.fThreads) threadsM+=0.3; });

  // Ленты
  const hasTape69 =activeNodes.some(nd=>nd.fTape69);
  const hasTape130=activeNodes.some(nd=>nd.fTape130);

  // ===== СБОРКА СПЕЦИФИКАЦИИ =====
  // 1. Плетёнка (ПЛМ)
  Object.entries(plmMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([nm,len])=>{
    spec.push([n++,fmtPLM(nm),'м',ru1(len)]);
  });
  // 2. Кабель
  Object.entries(cables).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([wt,total])=>{
    spec.push([n++,`${wt} ТУ 16-505.437-82`,'м',Math.ceil(total)]);
  });
  // 3. Провод
  Object.entries(wires).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([wt,total])=>{
    spec.push([n++,`${wt} ТУ 16-505.437-82`,'м',Math.ceil(total)]);
  });
  // 4. Оплётка PET
  Object.entries(petMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([nm,ln])=>{
    spec.push([n++,`Оплётка кабельная ${nm} Raychman`,'м',ru1(ln)]);
  });
  // 5. Трубка маркировочная
  Object.entries(markMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([k,q])=>spec.push([n++,k,'шт.',q]));
  Object.entries(lbMarkMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([k,q])=>spec.push([n++,k,'шт.',q]));
  // 6. ТТ (RBF) — на контакты
  if(ttContacts>0) spec.push([n++,'Трубка термоусаживаемая RBF Raychman 1.6/0.8 L=(12±1) мм черная','шт.',ttContacts]);
  // 7. ТТ с клеем (TCT)
  Object.entries(glueMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([k,q])=>spec.push([n++,k,'шт.',q]));
  Object.entries(lbGlueMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([k,q])=>spec.push([n++,k,'шт.',q]));
  // 7.5 Этикетки
  Object.entries(lbStickerMap).sort((a,b)=>a[0].localeCompare(b[0],'ru')).forEach(([k,q])=>spec.push([n++,k,'шт.',q]));
  // 8. Нитки
  if(threadsM>0) spec.push([n++,'Нитки специальные 3К, ОСТ 17-330-2002','м',+threadsM.toFixed(1)]);
  // 9. Лента 69
  if(hasTape69)  spec.push([n++,'Лента 3М Scotch 69','м',1.0]);
  // 10. Лента 130С
  if(hasTape130) spec.push([n++,'Лента самослипающаяся 3М Scotch 130С','м',1.0]);

  // ===== ВЫВОД =====
  const win=window.open('','_blank','width=900,height=680');
  win.document.write(`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Спецификация</title>
  <style>
  body{font-family:Arial,sans-serif;padding:24px;background:#fff;color:#222;}
  h2{margin-bottom:4px;font-size:16px;}
  .sub{font-size:11px;color:#888;margin-bottom:16px;}
  table{border-collapse:collapse;width:100%;}
  th{background:#1F4E79;color:#fff;padding:8px 12px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.5px;}
  td{padding:7px 12px;border-bottom:1px solid #eee;font-size:12px;}
  tr:nth-child(even) td{background:#f5f8ff;}
  .qty{font-weight:700;color:#1F4E79;font-family:monospace;}
  .unit{color:#888;font-size:11px;}
  </style></head><body>
  <h2>Спецификация материалов</h2>
  <div class="sub">Разъёмы: ${activeNodes.map(nn=>nn.name).join(', ')}${activeLabels.length?' · Бирки: '+activeLabels.map(l=>l.name).join(', '):''}</div>
  <table><thead><tr><th style="width:36px">№</th><th>Наименование / Обозначение</th><th style="width:60px">Ед.</th><th style="width:70px">Кол-во</th></tr></thead><tbody>
  ${spec.map(([num,name,unit,qty])=>`<tr><td style="text-align:center;color:#aaa">${num}</td><td>${name}</td><td class="unit" style="text-align:center">${unit}</td><td class="qty" style="text-align:center">${qty}</td></tr>`).join('')}
  </tbody></table>
  </body></html>`);
  win.document.close();
}

// ===== Инициализация =====
function buildWireSelect(){
  const groups={
    'МГТФ (фторопласт)':[
      'МГТФ 0,03','МГТФ 0,05','МГТФ 0,07','МГТФ 0,08(1x0.07)','МГТФ 0,08(1x0.10)','МГТФ 0,08(1х0.12)',
      'МГТФ 0,12(1х0.2)','МГТФ 0,12','МГТФ 0,14(1x0.14)','МГТФ 0,15(1х0.35)','МГТФ 0,20','МГТФ 0,35',
      'МГТФ 0,50','МГТФ 0,75','МГТФ 1','МГТФ 2x0.07','МГТФ 2x0.12'
    ],
    'МГТФЭ (экранированный)':[
      'МГТФЭ 0,07','МГТФЭ 0.08(1х12)','МГТФЭ 0.08(2х07)','МГТФЭ 0.08(2х12)','МГТФЭ 0.08(3х12)',
      'МГТФЭ 2x0.20','МГТФЭ 2x0.35','МГТФЭ 2x0.5','МГТФЭ 4x0.5'
    ],
    'МГШВ':['МГШВ 0.14','МГШВ 0.2','МГШВ 0.35','МГШВ 0.5','МГШВ 0.75','МГШВ 1','МГШВ 1.5'],
    'МГШВЭ (экранированный)':['МГШВЭ 0.14','МГШВЭ 0.2','МГШВЭ 0.35','МГШВЭ 0.5','МГШВЭ 0.75'],
    'НВ-3':['НВ-3 0.75','НВ-3 1.5'],
    'НВ-600':['НВ-600(бел.) 0.35','НВ-600 0.08','НВ-600 0.12','НВ-600 0.2','НВ-600 0.35','НВ-600 0.5','НВ-600 0.75','НВ-600 1','НВ-600 1.5','НВ-600 2.5'],
    'НВ-1000':['НВ-1000 0.08','НВ-1000 0.12','НВ-1000 0.2','НВ-1000 0.35','НВ-1000 0.5','НВ-1000 0.75','НВ-1000 1','НВ-1000 1.5','НВ-1000 2.5'],
    'ПВМП':['ПВМП-2 0.12','ПВМП-2.5 0.35'],
    'ПВС / ПЩ':['ПВС 3х2.5','ПЩ 0.5'],
    'Ethernet':['Ethernet_кат.5е U/UTP_24AWG','Ethernet_кат.5е F/UTP_24AWG_PVC','Ethernet_кат.5е SF/UTP_26/7AWG_PVC']
  };
  const sel=document.getElementById('epWire');
  sel.innerHTML='';
  Object.entries(groups).forEach(([label,list])=>{
    const og=document.createElement('optgroup');og.label=label;
    list.forEach(w=>{
      const o=document.createElement('option');o.value=w;o.textContent=w;
      og.appendChild(o);
    });
    sel.appendChild(og);
  });
}

window.onload=()=>{
  buildWireSelect();
  addNode({name:'Х1',type:'Вилка 5787775-1 с кожухом 5788362-1',contacts:68,marking:'"B"'});
  addNode({name:'Х2',type:'Розетка DB-37F с кожухом DP-37C2',contacts:34,marking:'"1"'});
  addNode({name:'Х3',type:'Розетка DB-37F с кожухом DP-37C2',contacts:34,marking:'"2"'});
  addNode({name:'Х4',contacts:20,marking:''});
  addNode({name:'Х5',contacts:16,marking:''});
  addNode({name:'Х6',contacts:12,marking:''});
};
</script>
</body>
</html>
