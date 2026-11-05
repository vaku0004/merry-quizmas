// node shoot_mobile.js <page.html> <outdir> <width> <height>
const {chromium}=require('playwright');const [,,PAGE,OUT,W,H]=process.argv;
const teams=[{name:"Team Elves",score:1100},{name:"Team Reindeer",score:-300},{name:"Team Snowmen",score:900},{name:"Team Gingerbread",score:400}];
const used={"0-0-0":1,"0-1-0":1,"0-2-1":1};
const base={screen:"board",teamCount:4,teams,round:0,used,turn:1,q:null,final:null,sound:false};
const shots=[
 ["01-setup",null],
 ["02-rules",{...base,screen:"rules",deck:"intro",slide:1,rulesReturn:false}],
 ["03-board",{...base}],
 ["04-board-r2",{...base,round:1,used:{}}],
 ["05-question",{...base,q:{c:2,i:3,value:400,special:null,picker:1,team:1,bid:null,judged:{},stage:"ask"}}],
 ["06-answer",{...base,q:{c:2,i:3,value:400,special:null,picker:1,team:1,bid:null,judged:{1:"ok"},stage:"answer"}}],
 ["07-cat",{...base,q:{c:1,i:3,value:400,special:"cat",picker:0,team:null,bid:null,judged:{},stage:"intro",catAsk:true}}],
 ["08-witch",{...base,q:{c:4,i:2,value:300,special:"witch",picker:0,team:null,bid:300,w:{price:300,team:2},judged:{},stage:"intro",witchAsk:true}}],
 ["09-final",{...base,screen:"final",round:1,used:{},final:{stage:"category",wagers:[],judged:[]}}],
 ["10-final-answer",{...base,screen:"final",round:1,used:{},final:{stage:"answer",wagers:[500,0,400,200],judged:["ok","no",null,null]}}],
 ["11-podium",{...base,screen:"podium",round:1,used:{},final:{stage:"done",wagers:[],judged:[]},teams:[{name:"Team Elves",score:3400},{name:"Team Reindeer",score:2100},{name:"Team Snowmen",score:2800},{name:"Team Gingerbread",score:900}]}],
 ["12-editor",{...base,screen:"setup",editor:{tab:0}}],
];
(async()=>{const b=await chromium.launch();const res=[];
 for(const [name,st] of shots){const ctx=await b.newContext({viewport:{width:+W,height:+H},deviceScaleFactor:1,isMobile:true,hasTouch:true});const p=await ctx.newPage();
  await p.goto(require('url').pathToFileURL(require('path').resolve(PAGE)).href);await p.evaluate(s=>{localStorage.clear();if(s)localStorage.setItem("mq-state-v1",JSON.stringify(s));},st);
  await p.reload();await p.waitForTimeout(600);
  const m=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,sh:document.documentElement.scrollHeight,
    wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+1&&getComputedStyle(e).position!=='fixed'}).slice(0,3).map(e=>e.className||e.tagName)}));
  res.push(name+' '+JSON.stringify(m));
  await p.screenshot({path:`${OUT}/${name}.png`,fullPage:true});await ctx.close();}
 console.log(res.join('\n'));await b.close();})();
