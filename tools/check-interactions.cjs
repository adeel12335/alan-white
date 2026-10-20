// Exercise the shipped search/filter code against the actual journal titles.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'blog.html'), 'utf8');
const decode = s => s.replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&#8217;/g, '’');
function element(text='') {
  return {textContent:text,hidden:false,style:{},attrs:{},events:{},classList:{toggle(){}},setAttribute(k,v){this.attrs[k]=v},getAttribute(k){return this.attrs[k]},addEventListener(k,v){this.events[k]=v}};
}
const posts=[],notes=[];
for(const match of html.matchAll(/<li class="post ([^"]*)">([\s\S]*?)<\/li>/g)) {
 const heading=element(decode(match[2].match(/<h2[^>]*>([\s\S]*?)<\/h2>/)[1]));
 const el=element(heading.textContent);el.querySelector=()=>heading;
 (match[1].includes('note-row')?notes:posts).push(el);
}
const search=element(); search.value='';
const count=element(); const empty=element();
const topics=['all','being','ssp','corrigenda'].map(topic=>{const e=element();e.attrs['data-topic']=topic;return e});
const selectors={'.posts .post:not(.note-row)':posts,'.posts .note-row':notes,'[data-topic]':topics};
const document={querySelector(s){return {'#post-search':search,'#post-count':count,'.empty':empty}[s]||null},querySelectorAll(s){return selectors[s]||[]},addEventListener(){}};
const window={scrollY:0,innerHeight:800,addEventListener(){}};
vm.runInNewContext(fs.readFileSync(path.join(root,'script.js'),'utf8'),{document,window});
function query(value){search.value=value;search.events.input();}
function topic(value){topics.find(t=>t.attrs['data-topic']===value).events.click();}
assert.equal(posts.length,12); assert.equal(notes.length,1);
query('');assert.equal(count.textContent,12);
topic('being');assert.equal(count.textContent,9);
topic('ssp');assert.equal(count.textContent,5);
topic('corrigenda');assert.equal(count.textContent,2);
query('Structure');assert.equal(count.textContent,1);
topic('all');query('17 Sept');assert.equal(count.textContent,0);assert.equal(notes[0].hidden,false);assert.equal(empty.style.display,'none');
query('no-such-paper-xyz');assert.equal(count.textContent,0);assert.equal(empty.style.display,'block');
query('');assert.equal(count.textContent,12);assert.equal(empty.style.display,'none');
assert.equal(topics.filter(b=>b.attrs['aria-pressed']==='true').length,1);
console.log('Journal checks passed: all topics, combined search, notes-only result, empty state, reset and filter accessibility.');
