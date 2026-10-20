const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
assert.equal((html.match(/data-slide role=/g)||[]).length,3);
function element(attrs={}){
 const classes=new Set();
 return {attrs,events:{},inert:false,textContent:'',classList:{add(x){classes.add(x)},toggle(x,on){if(on)classes.add(x);else classes.delete(x)},contains(x){return classes.has(x)}},getAttribute(k){return this.attrs[k]},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.events[k]=v}};
}
function fixture(reduced=false){
 const slides=[element(),element(),element()];
 const tabs=['Structural-Systematic Philosophy','Publications','Podcasts'].map((name,i)=>element({'data-slide-to':String(i),'aria-label':`Show slide ${i+1}: ${name}`}));
 const previous=element(),next=element(),pause=element(),icon=element(),status=element();
 const carousel=element();
 carousel.querySelectorAll=s=>s==='[data-slide]'?slides:tabs;
 carousel.querySelector=s=>({'[data-slide-prev]':previous,'[data-slide-next]':next,'[data-slide-pause]':pause,'[data-pause-icon]':icon,'[data-slide-status]':status}[s]);
 carousel.contains=x=>x===next||x===pause||x===previous;
 const document={hidden:false,events:{},querySelector:()=>carousel,addEventListener(k,v){this.events[k]=v}};
 const timers=new Map();let id=0;
 const window={matchMedia:()=>({matches:reduced,addEventListener(){}}),clearTimeout:i=>timers.delete(i),setTimeout:fn=>{timers.set(++id,fn);return id}};
 vm.runInNewContext(fs.readFileSync(path.join(root,'showcase.js'),'utf8'),{document,window,Array,Number,String});
 const active=()=>slides.findIndex(s=>s.classList.contains('is-active'));
 const tick=()=>{const [key,fn]=[...timers.entries()][0];timers.delete(key);fn()};
 return {slides,tabs,previous,next,pause,icon,status,carousel,document,timers,active,tick};
}
const f=fixture();
assert.equal(f.active(),0);assert.equal(f.timers.size,1);
f.previous.events.click();assert.equal(f.active(),2);
f.next.events.click();assert.equal(f.active(),0);
f.tabs[1].events.click();assert.equal(f.active(),1);assert.match(f.status.textContent,/2 of 3: Publications/);
assert.equal(f.slides[1].inert,false);assert.equal(f.slides[0].inert,true);
assert.equal(f.slides[0].attrs['aria-hidden'],'true');
f.tick();assert.equal(f.active(),2);assert.equal(f.timers.size,1);
f.pause.events.click();assert.equal(f.timers.size,0);assert.equal(f.pause.attrs['aria-label'],'Play slideshow');
f.pause.events.click();assert.equal(f.timers.size,1);
f.carousel.events.mouseenter();assert.equal(f.timers.size,0);
f.carousel.events.mouseleave();assert.equal(f.timers.size,1);
f.carousel.events.focusin();assert.equal(f.timers.size,0);
f.carousel.events.focusout({relatedTarget:null});assert.equal(f.timers.size,1);
f.document.hidden=true;f.document.events.visibilitychange();assert.equal(f.timers.size,0);
f.document.hidden=false;f.document.events.visibilitychange();assert.equal(f.timers.size,1);
f.carousel.events.keydown({key:'ArrowRight',preventDefault(){}});assert.equal(f.active(),0);
f.carousel.events.touchstart({touches:[{clientX:200,clientY:50}],target:{closest:()=>null}});
f.carousel.events.touchend({changedTouches:[{clientX:80,clientY:55}]});assert.equal(f.active(),1);
assert.equal(f.tabs.filter(t=>t.attrs['aria-pressed']==='true').length,1);
const r=fixture(true);assert.equal(r.timers.size,0);assert.equal(r.pause.attrs['aria-label'],'Play slideshow');
console.log('Carousel passed: 3 slides, wraparound, direct selection, autoplay, pause/play, hover/focus/background pause, keyboard, swipe and reduced motion.');
