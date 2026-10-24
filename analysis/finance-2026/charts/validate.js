const es=require('/home/user/YatraContentSeptember2026/node_modules/esbuild');const fs=require('fs');
for (const f of process.argv.slice(2)) {
  const s=fs.readFileSync(f,'utf8');
  es.transform(s,{loader:'tsx',jsx:'preserve'}).then(()=>console.log(f,'OK')).catch(e=>console.log(f,JSON.stringify(e.errors.map(x=>[x.text,x.location&&x.location.column,x.location&&x.location.lineText.slice(Math.max(0,x.location.column-60),x.location.column+20)]))));
}
