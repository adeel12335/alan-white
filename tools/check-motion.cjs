const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function el(){return {events:{},attrs:{},style:{},classList:{add(){}},addEventListener(k,f){this.events[k]=f},setAttribute(k,v){this.attrs[k]=v},contains(){return false}}}
const region=el(),viewport=el(),count=el(),progress=el(),pause=el(),prev=el(),next=el(),pagination=el();
region.querySelector=s=>({'[data-pathways-count]':count,'[data-pathway-progress]':progress,'[data-pathways-pause]':pause,'[data-pathways-prev]':prev,'[data-pathways-next]':next,'.pathways-pagination':pagination}[s]);
const document={hidden:false,events:{},querySelector:s=>s==='.pathways-motion'?region:viewport,addEventListener(k,f){this.events[k]=f}};
let swiper,options;
function Swiper(target,config){assert.equal(target,viewport);options=config;swiper=this;this.realIndex=0;this.params=config;this.autoplay={running:false,start(){this.running=true},stop(){this.running=false}};this.slideNext=()=>{this.realIndex=(this.realIndex+1)%3;config.on.slideChange.call(this)};this.slidePrev=()=>{this.realIndex=(this.realIndex+2)%3;config.on.slideChange.call(this)};}
const window={Swiper,matchMedia:()=>({matches:false,addEventListener(){}})};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../motion.js'),'utf8'),{window,document,String});
assert.equal(options.loop,false);assert.equal(options.rewind,true);assert.equal(options.centeredSlides,false);assert.equal(options.slidesPerView,1);assert.equal(options.breakpoints[1000].slidesPerView,2);assert.equal(options.effect,'slide');assert.equal(swiper.autoplay.running,true);assert.equal(count.textContent,'01 / 03');
viewport.events.keydown({key:'ArrowRight',preventDefault(){}});assert.equal(count.textContent,'02 / 03');
pause.events.click();assert.equal(swiper.autoplay.running,false);assert.equal(pause.attrs['aria-pressed'],'true');
pause.events.click();assert.equal(swiper.autoplay.running,true);
region.events.focusin();assert.equal(swiper.autoplay.running,false);
region.events.focusout({relatedTarget:null});assert.equal(swiper.autoplay.running,true);
document.hidden=true;document.events.visibilitychange();assert.equal(swiper.autoplay.running,false);
document.hidden=false;document.events.visibilitychange();assert.equal(swiper.autoplay.running,true);
assert.match(options.pagination.renderBullet(2,'bullet'),/Show section 3/);
assert.equal(options.navigation.prevEl,prev);assert.equal(options.navigation.nextEl,next);
console.log('Discovery carousel controller passed: responsive configuration, keyboard, counter, pause/play, focus pause, hidden-tab pause and pagination.');
