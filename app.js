let mode="current", data=null;
const files={current:"data/current/current_rating.json",historical:"data/historical/historical_rating.json",live:"data/current/live_rating.json"};
async function load(){data=await (await fetch(files[mode]+"?v="+Date.now())).json(); render();}
function sortedRows(){const factor=document.querySelector("#factor").value; let rows=[...data.rankings];
if(factor==="rating") rows.sort((a,b)=>b.rating-a.rating);
else rows.sort((a,b)=>(b.factors?.[factor]??0)-(a.factors?.[factor]??0));
rows.forEach((r,i)=>r.displayRank=i+1); return rows;}
function render(){const page=+document.querySelector("#page").value; const rows=sortedRows().slice(page*50,page*50+50);
document.querySelector("#status").textContent=`Engine ${data.meta.engine_version} / ${data.meta.generated_on} / ${data.meta.source_counts.games} games`;
document.querySelector("#rows").innerHTML=rows.map(r=>`<tr><td>${r.displayRank}</td><td><a href="#">${r.school_name}</a></td><td>${(r.rating??0).toFixed(2)}</td><td>${((r.win_rate??.5)*100).toFixed(1)}%</td><td>${(r.run_diff_per_game??0).toFixed(2)}</td><td>${(r.factors?.inning_stability??50).toFixed(1)}</td></tr>`).join("");}
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{mode=b.dataset.mode;document.querySelectorAll("nav button").forEach(x=>x.classList.remove("active"));b.classList.add("active");load();});
document.querySelector("#factor").onchange=render; document.querySelector("#page").onchange=render; document.querySelector('nav button[data-mode="current"]').classList.add("active"); load().catch(e=>document.querySelector("#status").textContent="JSONを読み込めません: "+e);
