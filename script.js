(function(){
var h=document.documentElement;
/* idioma */
var bs=document.querySelectorAll('.lang button');
function setL(l){h.setAttribute('data-lang',l);h.lang=l==='en'?'en':'pt-BR';bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l)});try{localStorage.setItem('lang',l)}catch(e){}}
if(bs.length){var l='pt';try{l=localStorage.getItem('lang')||((navigator.language||'').toLowerCase().indexOf('pt')===0?'pt':'en')}catch(e){}
 setL(l);bs.forEach(function(b){b.addEventListener('click',function(){setL(b.dataset.l);agora()})})}
/* aberto agora: horário no fuso do negócio */
var A=window.AGENDA||{},Z=window.TZ;
function local(){try{var p=new Intl.DateTimeFormat('en-US',{timeZone:Z,weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()),o={};p.forEach(function(x){o[x.type]=x.value});
 var d={Mon:0,Tue:1,Wed:2,Thu:3,Fri:4,Sat:5,Sun:6}[o.weekday];return{d:d,m:(+o.hour%24)*60+(+o.minute)}}catch(e){return null}}
function mm(s){var a=s.split(':');return +a[0]*60+(+a[1])}
function fmt(s,en){var a=s.split(':'),H=+a[0],M=a[1];if(es)return H+':'+M;if(!en)return H+'h'+(M!=='00'?M:'');var ap=H>=12?'pm':'am',h12=H%12||12;return h12+(M!=='00'?':'+M:'')+' '+ap}
var DS=['lunes','martes','miércoles','jueves','viernes','sábado','domingo'],es=false,DP=['segunda','terça','quarta','quinta','sexta','sábado','domingo'],DE=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
function agora(){var el=document.querySelector('[data-agora]');var t=local();if(!el||!t||!Object.keys(A).length)return;
 var en=h.getAttribute('data-lang')==='en',fx=A[t.d]||[],txt=null,ab=false;es=h.getAttribute('data-lang')==='es';
 if(window.H24){ab=true;txt=es?'Abierto ahora, 24 horas':en?'Open now, 24 hours':'Aberto agora, 24 horas'}
 for(var i=0;!txt&&i<fx.length;i++){if(t.m>=mm(fx[i][0])&&t.m<mm(fx[i][1])){ab=true;txt=(es?'Abierto ahora, cierra a las ':en?'Open now, closes at ':'Aberto agora, fecha às ')+fmt(fx[i][1],en)}}
 if(!txt){for(var k=0;k<8&&!txt;k++){var d=(t.d+k)%7,f=A[d]||[];for(var j=0;j<f.length;j++){if(k>0||mm(f[j][0])>t.m){
   var q=k===0?(es?'hoy':en?'today':'hoje'):k===1?(es?'mañana':en?'tomorrow':'amanhã'):(es?'el '+DS[d]:en?DE[d]:DP[d]);txt=(es?'Cerrado ahora, abre ':en?'Closed now, opens ':'Fechado agora, abre ')+q+(es?' a las ':en?' at ':' às ')+fmt(f[j][0],en);break}}}}
 if(txt){el.textContent=txt;el.hidden=false;el.classList.toggle('aberto',ab)}
 document.querySelectorAll('.horas tr').forEach(function(r){var ds=(r.dataset.dias||'').split(',');r.classList.toggle('hoje',ds.indexOf(String(t.d))>-1)})}
agora();setInterval(agora,60000);
/* miniaturas do celular reaproveitam a foto do painel */
document.querySelectorAll('.thumb[data-de]').forEach(function(t){var s=t.closest('.serv'),f=s&&s.querySelector('.painel figure[data-i="'+t.dataset.de+'"] img');if(f){var i=new Image();i.src=f.src;i.alt='';i.decoding='async';t.appendChild(i)}});
/* serviços: a foto acompanha o item */
document.querySelectorAll('.serv').forEach(function(s){var ls=s.querySelectorAll('.linha[data-i]'),fs=s.querySelectorAll('.painel figure');if(!fs.length)return;
 function on(i){fs.forEach(function(f){f.classList.toggle('on',f.dataset.i===i)});ls.forEach(function(x){x.classList.toggle('on',x.dataset.i===i)})}
 ls.forEach(function(x){x.addEventListener('mouseenter',function(){on(x.dataset.i)});x.addEventListener('focus',function(){on(x.dataset.i)})});
 if(ls[0])ls[0].classList.add('on')});
})();
